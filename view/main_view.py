# Displays the data from the model, captures user's input and
# sends user commands to the controller to reflect actions based on their gestures
# Components: Methods for displaying video feed, drawing landmarks and additional visual feedback

from utils.gesture_checks import pips_above_mcps, additional_landmark_checks, hand_angle_validation
import cv2

class MainView:
    def __init__(self, hand_detector, window_manager, gesture_controller):
        '''
        Initialize the MainView object.

        Params:
            hand_detector (HandDetector): Instance of HandDetector for detecting hand landmarks
            window_manager (WindowManager): Instance of WindowManager for managing windows
            gesture_controller (GestureController): Instance of GestureController for handling gestures
        '''
        self.cap = cv2.VideoCapture(0)  # Open the webcam
        if not self.cap.isOpened():
            raise ValueError("Could not open webcam")
        
        self.hand_detector = hand_detector
        self.window_manager = window_manager
        self.gesture_controller = gesture_controller

    def display_frame(self, frame):
        '''
        Display a frame on the screen with detected hand landmarks and visual feedback

        Params:
            frame (numpy.ndarray): Frame from the webcam feed (BGR format)
        '''
        # Convert frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hand landmarks
        hand_landmarks = self.hand_detector.detect_single_hand(rgb_frame)

        if hand_landmarks:
            self.draw_feedback(frame, hand_landmarks)

        cv2.imshow("Hand Gesture Control", frame)

    def draw_feedback(self, image, hand_landmarks):
        '''
        Draw visual feedback on the image based on gesture validity

        Params:
            image (numpy.ndarray): Frame image to draw feedback on (BGR format)
            hand_landmarks (mediapipe Hands.Hand): Detected hand landmarks
        '''
        # Write visual text feedback whether hand position is valid. (Coordinates, style, size, Green text, thickness)
        if pips_above_mcps(hand_landmarks) and additional_landmark_checks(hand_landmarks) and hand_angle_validation(hand_landmarks):
            cv2.putText(image, "Valid Hand Position", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Invalid Hand Position", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 

    def run(self):
        '''
        Start capturing frames from the webcam, process gestures, and display feedback.
        '''
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Process gestures for the current frame
            self.gesture_controller.process_gestures(frame)

            self.display_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on pressing 'q'
                break

        self.cap.release()  # Release webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows
