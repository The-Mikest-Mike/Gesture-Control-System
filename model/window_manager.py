# Manages the data logic and interactions with the data
# Components: WindowManager

import pyautogui

class WindowManager:
    def __init__(self): # Initialize any necessary attributes
        pass 

    def close_frontmost_window(self):
        # Window closing logic using pyautogui
        try:
            pyautogui.hotkey('command', 'w') # Simulate 'Command + w' to close the frontmost window
        except Exception as e:
            print(f"Error Closing Window: {e}") # Debug: log exception while closing window

    def minimize_frontmost_window(self):
        # Window minimizing logic
        try:
            pyautogui.hotkey('command', 'm') # Simulate 'Command + m' to minimize the frontmost window
        except Exception as e:
            print(f"Exception Minimizing Window: {e}") # Debug: log exception while minimizing window

    def full_screen_frontmost_window(self):
        # Enter full screen logic
        try:
            pyautogui.hotkey('fn', 'f') # Simulate 'fn + f' to enter full screen with the frontmost window
        except Exception as e:
            print(f"Exception Full Screen Window: {e}") # Debug: log exception while entering full screen
        pass
