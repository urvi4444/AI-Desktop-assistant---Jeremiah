import os
import sys
import winshell
from win32com.client import Dispatch
import icon

def create_desktop_shortcut():
    # First create the icon
    icon.create_icon()
    
    # Get the path to the desktop
    desktop = winshell.desktop()
    
    # Get the path to the script
    script_path = os.path.abspath("gui.py")
    icon_path = os.path.abspath("jeremiah.ico")
    
    # Create the shortcut path
    shortcut_path = os.path.join(desktop, "Jeremiah Assistant.lnk")
    
    # Create the shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = sys.executable  # Python interpreter path
    shortcut.Arguments = f'"{script_path}"'  # Script path in quotes
    shortcut.IconLocation = icon_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.Description = "Jeremiah - Your AI Desktop Assistant"
    shortcut.save()
    
    print("Desktop shortcut created successfully!")

if __name__ == '__main__':
    create_desktop_shortcut()
