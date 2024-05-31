# This module defines the HandDetector class for detecting hands and gestures logic

import cv2
import pyautogui
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands() # Initialize the mediapipe hands module
        self.drawing_utils = mp.solutions.drawing_utils # Utility for drawing hand landmarks
        # Initialize coordinates for gesture detection
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def detect_hands(self, image):
        print("Detecting hands. . .") # Debug: log hand detectiion fuction being called
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert the image from BRG to RGB
        output = self.hands.process(rgb_image) # Process the image using mediapipe hands module
        hands = output.multi_hand_landmarks  # Get the detected hands
        # Ensure that 'detect_hands' returns a list instead of 'None' to avoid " 'NoneType' object is not iterable" error
        return hands if hands is not None else []


    def detect_close_gesture(self, hand):
        print("Detecting close gesture. . .") # Debug: log close gesture method being called
        # Implementation for detecting if pinky finger is in contact with the thumb (close gesture)
        pass

    def detect_minimize_gesture(self, hand):
        print("Detecting minimize gesture. . .") # Debug: log minimize gesture method being called
        # Implemention for detecting if ring finger is in contact with the thumb (minimize gesture)
        pass

    def detect_full_screen_gesture(self, hand):
        print("Detecting full screen gesture. . .")# Debug: log enter full screen gesture function being called
        # Implemention for detecting if the ring finger is in contact with the thumb (minimize gesture)
        pass

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


