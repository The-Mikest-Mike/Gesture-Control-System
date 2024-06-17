# Displays the data from the model, captures user's input and
# sends user commands to the controller to reflect actions based on their gestures
# Components: Methods for displaying video feed, drawing landmarks and aditional visual feedback

from utils.gesture_checks import pips_above_mcps, additional_landmark_checks, hand_angle_validation
import cv2

class MainView:
    def __init__(self, hand_detector, window_manager, gesture_controller):
        self.cap = cv2.VideoCapture(0)  # Open the webcam
        self.hand_detector = hand_detector
        self.window_manager = window_manager
        self.gesture_controller = gesture_controller

    def display_frame(self, frame):
        # Draw landmarks and gestures on the frame
        hand_landmarks = self.hand_detector.detect_single_hand(frame)
        if hand_landmarks:
            self.draw_feedback(frame, hand_landmarks)
        cv2.imshow("Hand Gesture Control", frame)
    
    def draw_feedback(self, image, hand_landmarks):
        # Write visual feedback wether gestures are valid
        if pips_above_mcps(hand_landmarks) and additional_landmark_checks(hand_landmarks) and hand_angle_validation(hand_landmarks):
            cv2.putText(image, "Valid Hand Position", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Coordinates, style, size, Green text, thickness
        else:
            cv2.putText(image, "Invalid Hand Position", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # Coordinates, style, size, Red text, thickness

    def run(self):
        frame = cv2.flip(frame, 1)  # Flip the image horizontally for a mirror effect
        self.gesture_controller.process_gestures(frame)  # Process gestures
        self.display_frame(frame)  # Display the frame
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            

