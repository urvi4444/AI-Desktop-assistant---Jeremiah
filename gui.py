import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading
import assistant as assistant_module

class Bubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.animation = QPropertyAnimation(self, b"pos")
        self.start_animation()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient for bubble
        gradient = QRadialGradient(20, 20, 20)
        gradient.setColorAt(0, QColor(255, 255, 255, 30))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 40, 40)
        
    def start_animation(self):
        start_x = QRandomGenerator.global_().bounded(self.parent().width() - 40)
        start_y = self.parent().height()
        end_x = QRandomGenerator.global_().bounded(self.parent().width() - 40)
        end_y = -40
        
        self.move(start_x, start_y)
        self.animation.setDuration(QRandomGenerator.global_().bounded(4000, 8000))
        self.animation.setStartValue(QPoint(start_x, start_y))
        self.animation.setEndValue(QPoint(end_x, end_y))
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self.restart_animation)
        self.animation.start()
        
    def restart_animation(self):
        if self.parent():
            self.start_animation()

class BubbleBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bubbles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_bubble)
        self.timer.start(2000)  # Add new bubble every 2 seconds
        
    def add_bubble(self):
        if len(self.bubbles) < 15:  # Limit number of bubbles
            bubble = Bubble(self)
            self.bubbles.append(bubble)
            bubble.show()
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        for bubble in self.bubbles:
            if not bubble.animation.state() == QAbstractAnimation.Running:
                bubble.start_animation()

class VoiceThread(QThread):
    textChanged = pyqtSignal(str)
    assistantResponse = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = True
    
    def run(self):
        while self._is_running:
            print("VoiceThread: Listening for command...")
            command = assistant_module.listen()
            if command:
                print(f"VoiceThread: Got command: {command}")
                self.textChanged.emit(command)
                threading.Thread(target=self.process_command, args=(command,)).start()
    
    def process_command(self, command):
        print(f"VoiceThread: Processing command: {command}")
        original_speak = assistant_module.speak
        def gui_speak(text):
            print(f"VoiceThread: Assistant response: {text}")
            self.assistantResponse.emit(text)
            original_speak(text)
        assistant_module.speak = gui_speak
        
        continue_listening = assistant_module.process_command(command)
        assistant_module.speak = original_speak
        
        if not continue_listening:
            self._is_running = False
            
    def stop(self):
        self._is_running = False
        self.terminate()

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.voice_thread = None
        self.is_listening = False

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Jeremiah Assistant')
        self.setGeometry(100, 100, 800, 600)
        
        # Create and set the central widget with bubble background
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create bubble background
        self.bubble_background = BubbleBackground(central_widget)
        self.bubble_background.setGeometry(0, 0, 800, 600)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Set window and widget styles with lighter colors
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f0ff,
                    stop:1 #e6d5ff);
            }
            QWidget {
                color: #4a0080;
            }
            QPushButton {
                background-color: rgba(138, 43, 226, 0.2);
                color: #4a0080;
                border: 2px solid rgba(138, 43, 226, 0.3);
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(138, 43, 226, 0.3);
                border: 2px solid rgba(138, 43, 226, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(138, 43, 226, 0.4);
            }
            QLabel {
                color: #4a0080;
            }
        """)

        # Create title with glass effect
        title_container = QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 20px;
                padding: 20px;
                border: 2px solid rgba(138, 43, 226, 0.2);
            }
        """)
        title_layout = QVBoxLayout(title_container)
        
        title_label = QLabel('Jeremiah')
        title_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #4a0080;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel('Your Friendly Desktop Assistant!!!')
        subtitle_label.setStyleSheet("""
            color: #6b2ba5;
            font-size: 18px;
            margin-bottom: 20px;
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        # Create conversation display with glass effect
        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        self.conversation.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.7);
                border: 2px solid rgba(138, 43, 226, 0.2);
                border-radius: 20px;
                padding: 20px;
                font-size: 16px;
                color: #4a0080;
            }
            QScrollBar:vertical {
                background-color: rgba(138, 43, 226, 0.1);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(138, 43, 226, 0.2);
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(138, 43, 226, 0.3);
            }
        """)

        # Create status label with glass effect
        self.status_label = QLabel('Ready to listen!')
        self.status_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.7);
            color: #4a0080;
            padding: 10px;
            border-radius: 15px;
            font-size: 16px;
            margin: 10px 0;
            border: 2px solid rgba(138, 43, 226, 0.2);
        """)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Create button with glass effect
        self.listen_button = QPushButton('Start Listening')
        self.listen_button.clicked.connect(self.toggle_listening)
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(138, 43, 226, 0.2);
                color: #4a0080;
                border: 2px solid rgba(138, 43, 226, 0.3);
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(138, 43, 226, 0.3);
                border: 2px solid rgba(138, 43, 226, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(138, 43, 226, 0.4);
            }
        """)

        # Add widgets to layout
        layout.addWidget(title_container)
        layout.addWidget(self.conversation)
        layout.addWidget(self.status_label)
        layout.addWidget(self.listen_button, alignment=Qt.AlignCenter)

        # Show initial greeting
        self.initial_greeting()

    def initial_greeting(self):
        welcome_message = """
        <div style='text-align: center; margin: 20px; background-color: rgba(255, 255, 255, 0.7); padding: 30px; border-radius: 20px; border: 2px solid rgba(138, 43, 226, 0.2);'>
            <span style='font-size: 28px; color: #4a0080; font-weight: bold;'>👋 Welcome to Jeremiah!</span><br><br>
            <span style='color: #6b2ba5; font-size: 18px;'>I'm your friendly desktop assistant, ready to help you with:</span><br><br>
            <div style='background-color: rgba(255, 255, 255, 0.5); padding: 20px; border-radius: 15px; margin: 10px 0; border: 1px solid rgba(138, 43, 226, 0.1);'>
                <span style='color: #4a0080; font-size: 16px;'>• Web apps: WhatsApp, Gmail, YouTube, Drive, Maps</span><br>
                <span style='color: #5c1a99; font-size: 16px;'>• Social: Facebook, Instagram, Twitter, LinkedIn</span><br>
                <span style='color: #6b2ba5; font-size: 16px;'>• System apps: Word, Excel, PowerPoint, Notepad</span><br>
                <span style='color: #7a3cb2; font-size: 16px;'>• Files: Open any file on your computer</span><br>
                <span style='color: #8a4dbf; font-size: 16px;'>• Other: Weather, Time, Web Search, Music</span><br>
                <span style='color: #9964cc; font-size: 16px;'>• And much more!</span>
            </div><br>
            <span style='color: #4a0080; font-size: 18px; font-weight: bold;'>Just click 'Start Listening' and ask me anything!</span>
        </div>
        """
        self.conversation.setHtml(welcome_message)
        assistant_module.greet()

    def update_conversation(self, message, is_user=False):
        current_html = self.conversation.toHtml()
        style = "color: rgba(255, 255, 255, 0.9); margin: 5px 0;" if is_user else "color: #4a0080; margin: 5px 0;"
        prefix = "You: " if is_user else "Jeremiah: "
        new_message = f"<div style='{style}'><b>{prefix}</b>{message}</div>"
        
        if "Goodbye" in message:
            QTimer.singleShot(2000, self.initial_greeting)
        else:
            self.conversation.setHtml(current_html + new_message)

    def update_status(self, status):
        self.status_label.setText(status)

    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.is_listening = True
        self.listen_button.setText('Stop Listening')
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(138, 43, 226, 0.2);
                color: #4a0080;
                border: 2px solid rgba(138, 43, 226, 0.3);
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(138, 43, 226, 0.3);
                border: 2px solid rgba(138, 43, 226, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(138, 43, 226, 0.4);
            }
        """)
        self.voice_thread = VoiceThread(self)
        self.voice_thread.textChanged.connect(lambda x: self.update_conversation(x, True))
        self.voice_thread.assistantResponse.connect(lambda x: self.update_conversation(x, False))
        self.voice_thread.start()

    def stop_listening(self):
        self.is_listening = False
        self.listen_button.setText('Start Listening')
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(138, 43, 226, 0.2);
                color: #4a0080;
                border: 2px solid rgba(138, 43, 226, 0.3);
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(138, 43, 226, 0.3);
                border: 2px solid rgba(138, 43, 226, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(138, 43, 226, 0.4);
            }
        """)
        if self.voice_thread:
            self.voice_thread.stop()

def main():
    app = QApplication(sys.argv)
    ex = AssistantGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
