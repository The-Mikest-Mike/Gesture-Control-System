# Manages the data logic and interactions with the data
# Components: HandDetector

import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, min_detection_confidence=0.9, min_tracking_confidence=0.5):
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)  # Initialize the mediapipe hands module with confidence threshold
        self.drawing_utils = mp.solutions.drawing_utils  # Utility for drawing hand landmarks
        self.min_detection_confidence = min_detection_confidence  # Store the min_detection_confidence
        self.previous_hand_position = (0, 0)  # Initialize the previous hand position

    def detect_single_hand(self, image):
        print("Detecting hands...")  # Debug: log hand detection function being called
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
        output = self.hands.process(rgb_image)  # Process the image using mediapipe hands module
        hand_landmarks = output.multi_hand_landmarks  # Get the detected hands

        # Ensure that 'detect_single_hand' returns a single hand landmark
        if hand_landmarks:
            for hand_landmark in hand_landmarks:
                if hand_landmark.landmark and output.multi_handedness:
                    confidence_score = output.multi_handedness[0].classification[0].score
                    if confidence_score >= self.min_detection_confidence:
                        print(f"Confidence score reached: {confidence_score}, Handedness: {output.multi_handedness[0].classification[0].label}")  # Debug: log confidence score and handedness
                        return hand_landmark  # Return the first detected hand with sufficient confidence
        return None  # Return None if no hands are detected with sufficient confidence
