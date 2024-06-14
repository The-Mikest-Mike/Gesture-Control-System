# Manages the data logic and interactions with the data
# Components: HandDetector

import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, min_detection_confidence=0.9): # The confidence threshold that a hand is present. Fixed value [0.0 to 1.0]
        self.hands = mp.solutions.hands.Hands() # Initialize the mediapipe hands module
        self.drawing_utils = mp.solutions.drawing_utils # Utility for drawing hand landmarks
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0 # Initialize coordinates for gesture detection
        self.min_detection_confidence = min_detection_confidence # Store the min_detection_confidence
    
    def detect_single_hand(self, image):
        print("Detecting hands...")  # Debug: log hand detection function being called
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
        output = self.hands.process(rgb_image)  # Process the image using mediapipe hands module
        hand_landmarks = output.multi_hand_landmarks  # Get the detected hands

        # Ensure that 'detect_single_hand' returns a single hand landmarkw
        if hand_landmarks:
            # Iterate through the detected hand landmarks
            for hand_landmark in hand_landmarks:
                # - hand_landmark.landmark: Verifies that the detected hand landmarks are present.
                # - output.multi_handedness: Verifies whether the hand is left or right is available in the output.
                if hand_landmark.landmark and output.multi_handedness:
                    # Extract confidence score of the first detected hand
                    confidence_score = output.multi_handedness[0].classification[0].score
                    # Validates if confidence score meets or exceeds the minimum detection confidence threshold
                    if confidence_score >= self.min_detection_confidence:
                        print("Conficence score reached") # Debug: log min_detection_conficence threshold has been reached
                        return hand_landmark  # Return the first detected hand with sufficient confidence
        return None  # Return None if no hands are detected with sufficient confidence