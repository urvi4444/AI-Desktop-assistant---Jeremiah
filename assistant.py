import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyautogui
import pywhatkit
import requests
import json

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set male voice (index 0)
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

def speak(text):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

def listen():
    """Listen to user's voice input and convert to text"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing...")
            
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.WaitTimeoutError:
        print("Timeout waiting for speech")
        return None
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except Exception as e:
        print(f"Error in listen function: {e}")
        return None

def greet():
    """Greet the user based on time of day"""
    try:
        hour = datetime.datetime.now().hour
        greeting = "Good morning" if 4 <= hour < 12 else "Good afternoon" if 12 <= hour < 17 else "Good evening"
        speak(f"{greeting}! I'm Jeremiah, your desktop assistant. How can I help you today?")
    except Exception as e:
        print(f"Error in greet function: {e}")
        speak("Hello! I'm Jeremiah. How can I help you today?")

def get_weather(city):
    """Get weather information for a city"""
    api_key = "YOUR_API_KEY"  # Replace with actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}"
    except:
        return "Sorry, I couldn't fetch the weather information"

def process_command(command):
    """Process user's voice command"""
    try:
        if command is None:
            speak("I didn't catch that. Could you please repeat?")
            return True

        print(f"Processing command: {command}")
        command = command.lower()

        # Web applications
        if "open whatsapp" in command:
            webbrowser.open("https://web.whatsapp.com")
            speak("Opening WhatsApp Web")
        elif "open gmail" in command:
            webbrowser.open("https://mail.google.com")
            speak("Opening Gmail")
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google")
        elif "open maps" in command:
            webbrowser.open("https://maps.google.com")
            speak("Opening Google Maps")
        elif "open drive" in command:
            webbrowser.open("https://drive.google.com")
            speak("Opening Google Drive")
        elif "open facebook" in command:
            webbrowser.open("https://facebook.com")
            speak("Opening Facebook")
        elif "open instagram" in command:
            webbrowser.open("https://instagram.com")
            speak("Opening Instagram")
        elif "open twitter" in command or "open x" in command:
            webbrowser.open("https://twitter.com")
            speak("Opening Twitter")
        elif "open linkedin" in command:
            webbrowser.open("https://linkedin.com")
            speak("Opening LinkedIn")
        elif "open github" in command:
            webbrowser.open("https://github.com")
            speak("Opening GitHub")

        # System applications
        elif "open notepad" in command:
            os.startfile("notepad.exe")
            speak("Opening Notepad")
        elif "open calculator" in command:
            os.startfile("calc.exe")
            speak("Opening Calculator")
        elif "open paint" in command:
            os.startfile("mspaint.exe")
            speak("Opening Paint")
        elif "open word" in command:
            try:
                os.startfile("WINWORD.EXE")
                speak("Opening Microsoft Word")
            except:
                speak("Microsoft Word is not installed")
        elif "open excel" in command:
            try:
                os.startfile("EXCEL.EXE")
                speak("Opening Microsoft Excel")
            except:
                speak("Microsoft Excel is not installed")
        elif "open powerpoint" in command:
            try:
                os.startfile("POWERPNT.EXE")
                speak("Opening Microsoft PowerPoint")
            except:
                speak("Microsoft PowerPoint is not installed")
        elif "open chrome" in command:
            try:
                os.startfile("chrome.exe")
                speak("Opening Google Chrome")
            except:
                speak("Google Chrome is not installed")
        elif "open edge" in command:
            try:
                os.startfile("msedge.exe")
                speak("Opening Microsoft Edge")
            except:
                speak("Microsoft Edge is not installed")

        # File operations
        elif "open file" in command:
            try:
                # Extract file name from command
                file_name = command.replace("open file", "").strip()
                if not file_name:
                    speak("Please specify a file name to open")
                    return True
                
                # Search in all drives
                drives = [d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f'{d}:')]
                found = False
                
                # Common file extensions to try
                extensions = ['', '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png']
                
                for drive in drives:
                    if found:
                        break
                    
                    base_paths = [
                        f"{drive}:\\",
                        f"{drive}:\\Users\\{os.getenv('USERNAME')}\\Desktop",
                        f"{drive}:\\Users\\{os.getenv('USERNAME')}\\Documents",
                        f"{drive}:\\Users\\{os.getenv('USERNAME')}\\Downloads",
                    ]
                    
                    for base_path in base_paths:
                        if not os.path.exists(base_path):
                            continue
                            
                        # First try exact match
                        for ext in extensions:
                            full_path = os.path.join(base_path, file_name + ext)
                            if os.path.exists(full_path):
                                try:
                                    os.startfile(full_path)
                                    speak(f"Opening {os.path.basename(full_path)}")
                                    found = True
                                    break
                                except Exception as e:
                                    print(f"Failed to open {full_path}: {e}")
                                    continue
                        
                        if found:
                            break
                            
                        # If exact match not found, try searching in subdirectories
                        try:
                            for root, _, files in os.walk(base_path):
                                for file in files:
                                    if file_name.lower() in file.lower():
                                        full_path = os.path.join(root, file)
                                        try:
                                            os.startfile(full_path)
                                            speak(f"Opening {file}")
                                            found = True
                                            break
                                        except Exception as e:
                                            print(f"Failed to open {full_path}: {e}")
                                            continue
                                if found:
                                    break
                        except Exception as e:
                            print(f"Error searching in {base_path}: {e}")
                            continue
                        
                        if found:
                            break
                
                if not found:
                    speak(f"Sorry, I couldn't find the file {file_name}")
            except Exception as e:
                print(f"Error opening file: {e}")
                speak("Sorry, I had trouble opening that file")
            return True

        elif "wikipedia" in command:
            speak("Searching Wikipedia...")
            query = command.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("Sorry, I couldn't find that on Wikipedia")

        elif "time" in command:
            time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {time}")

        elif "weather" in command:
            speak("Which city would you like to know the weather for?")
            city = listen()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)

        elif "play" in command:
            song = command.replace("play", "")
            speak(f"Playing {song} for you")
            pywhatkit.playonyt(song)

        elif "search" in command:
            search_term = command.replace("search", "")
            webbrowser.open(f"https://google.com/search?q={search_term}")
            speak(f"Here are the search results for {search_term}")

        elif "exit" in command or "goodbye" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            return False
        else:
            speak("I'm not sure how to help with that. Could you try something else?")

        return True
    except Exception as e:
        print(f"Error in process_command: {e}")
        speak("I encountered an error. Please try again.")
        return True

if __name__ == "__main__":
    greet()
    running = True
    while running:
        command = listen()
        running = process_command(command)
