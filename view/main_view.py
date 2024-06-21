# Displays the data from the model, captures user's input and
# sends user commands to the controller to reflect actions based on their gestures
# Components: Methods for displaying video feed, drawing landmarks and additional visual feedback

from utils.gesture_checks import pips_above_mcps, additional_landmark_checks, hand_angle_validation
import cv2

import cv2
from utils.gesture_checks import pips_above_mcps, additional_landmark_checks, hand_angle_validation

class MainView:
    def __init__(self, hand_detector, window_manager, gesture_controller):
        self.cap = cv2.VideoCapture(0)  # Open the webcam
        if not self.cap.isOpened():
            raise ValueError("Could not open webcam")
        self.hand_detector = hand_detector
        self.window_manager = window_manager
        self.gesture_controller = gesture_controller

    def display_frame(self, frame):
        # Convert frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hand landmarks
        hand_landmarks = self.hand_detector.detect_single_hand(rgb_frame)

        if hand_landmarks:
            self.draw_feedback(frame, hand_landmarks)

        cv2.imshow("Hand Gesture Control", frame)

    def draw_feedback(self, image, hand_landmarks):
        # Write visual feedback whether gestures are valid
        if pips_above_mcps(hand_landmarks) and additional_landmark_checks(hand_landmarks) and hand_angle_validation(hand_landmarks): 
            cv2.putText(image, "Valid Hand Position", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Coordinates, style, size, Green text, thickness
        else:
            cv2.putText(image, "Invalid Hand Position", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # Coordinates, style, size, Green text, thickness

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Process gestures for the current frame
            self.gesture_controller.process_gestures(frame) # Process gestures

            self.display_frame(frame) # Display the frame

            if cv2.waitKey(1) & 0xFF == ord('q'): # Exit on pressing 'q'
                break

        self.cap.release() # Release webcam
        cv2.destroyAllWindows() # Close all OpenCV windows
