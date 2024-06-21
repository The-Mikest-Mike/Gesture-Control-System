# Manages the data logic and interactions with the data
# Components: HandDetector

import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, min_detection_confidence=0.9, min_tracking_confidence=0.5):
        '''
        Initializes the HandDetector with specified confidence thresholds
        
        Args:
            min_detection_confidence (float): Minimum confidence value for hand detection
            min_tracking_confidence (float): Minimum confidence value for hand tracking
        '''
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)  # Initialize the mediapipe hands module with confidence thresholds
        self.drawing_utils = mp.solutions.drawing_utils  # Utility for drawing hand landmarks
        self.min_detection_confidence = min_detection_confidence  # Store the minimum detection confidence
        self.previous_hand_position = (0, 0)  # Initialize the previous hand position

    def detect_single_hand(self, image):
        '''
        Detects a single hand in the provided image
        
        Args:
            image (numpy.ndarray): The input image in which to detect hands
        
        Returns:
            hand_landmark: The detected hand landmark if confidence score is sufficient, else None
        '''
        print("Detecting hands...")  # Debug: Log hand detection function being called
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
        output = self.hands.process(rgb_image)  # Process the image using the mediapipe hands module
        hand_landmarks = output.multi_hand_landmarks  # Get the detected hand landmarks

        # Ensure that 'detect_single_hand' returns a single hand landmark
        if hand_landmarks:
            for hand_landmark in hand_landmarks:
                if hand_landmark.landmark and output.multi_handedness:
                    confidence_score = output.multi_handedness[0].classification[0].score  # Get the confidence score of the detected hand
                    if confidence_score >= self.min_detection_confidence:
                        print(f"Confidence score reached: {confidence_score}, Handedness: {output.multi_handedness[0].classification[0].label}")  # Debug: Log confidence score and handedness
                        return hand_landmark  # Return the first detected hand with sufficient confidence
        return None  # Return None if no hands are detected with sufficient confidence
