# Manages the data logic and interactions with the data
# Components: HandDetector

import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands() # Initialize the mediapipe hands module
        self.drawing_utils = mp.solutions.drawing_utils # Utility for drawing hand landmarks
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0 # Initialize coordinates for gesture detection

    def detect_hands(self, image):
        print("Detecting hands. . .") # Debug: log hand detectiion fuction being called
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert the image from BRG to RGB
        output = self.hands.process(rgb_image) # Process the image using mediapipe hands module
        hands = output.multi_hand_landmarks  # Get the detected hands
        # Ensure that 'detect_hands' returns a list instead of 'None' to avoid " 'NoneType' object is not iterable" error
        return hands if hands is not None else []


    def detect_close_gesture(self, hand):
        print("Detecting close gesture. . .") # Debug: log close gesture method being called
        # From controller Implementation for detecting if pinky finger is in contact with the thumb (close gesture)
        pass

    def detect_minimize_gesture(self, hand):
        print("Detecting minimize gesture. . .") # Debug: log minimize gesture method being called
        # From controller Implemention for detecting if ring finger is in contact with the thumb (minimize gesture)
        pass

    def detect_full_screen_gesture(self, hand):
        print("Detecting full screen gesture. . .")# Debug: log enter full screen gesture function being called
        # From controller Implemention for detecting if the ring finger is in contact with the thumb (minimize gesture)
        pass



