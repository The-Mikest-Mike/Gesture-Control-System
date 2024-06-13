# Manages the data logic and interactions with the data
# Components: HandDetector

import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands() # Initialize the mediapipe hands module
        self.drawing_utils = mp.solutions.drawing_utils # Utility for drawing hand landmarks
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0 # Initialize coordinates for gesture detection
    
    def detect_single_hand(self, image):
        print("Detecting hands...")  # Debug: log hand detection function being called
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
        output = self.hands.process(rgb_image)  # Process the image using mediapipe hands module
        hand_landmarks = output.multi_hand_landmarks  # Get the detected hands

        # Ensure that 'detect_single_hand' returns a single hand landmarkw
        if hand_landmarks:
            return hand_landmarks[0]  # Return only the first detected hand
        else:
            return None  # Return None if no hands are detected