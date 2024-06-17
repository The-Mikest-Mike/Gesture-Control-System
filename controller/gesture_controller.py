# Acts as an intermediary between the model and the view. It listens to the input from the view, 
# processes it (using the model if necessary) and updates the view accordingly
# Have methods that are called by the view to perform actions and update the model
# Components: GestureController

import mediapipe as mp
from utils.gesture_checks import additional_landmark_checks, pips_above_mcps, hand_angle_validation
import time

class GestureController:
    def __init__(self, hand_detector, window_manager):
        self.hand_detector = hand_detector  # Instance of HandDetector for detecting hands
        self.window_manager = window_manager  # Instance of WindowManager for managing windows
        self.drawing_utils = mp.solutions.drawing_utils  # Utility for drawing hand landmarks
        self.valid_gesture_flag = False  # Initialize flag to indicate if initial validation is passed
        self.last_valid_time = None  # Initialize timestamp of the last valid gesture

    def process_gestures(self, image):
        print("Processing gestures...")  # Debug: log process_gestures function being called
        hand_landmark = self.hand_detector.detect_single_hand(image)  # Detect single hand in the provided image

        if hand_landmark:  # Check if a hand is detected
            print("Hand detected")
            self.drawing_utils.draw_landmarks(image, hand_landmark, mp.solutions.hands.HAND_CONNECTIONS)  # Draw landmarks on detected hand in 'image' by using the 'drawing_utils' object

            if self.valid_gesture_flag or (pips_above_mcps(hand_landmark) and additional_landmark_checks(hand_landmark) and hand_angle_validation(hand_landmark)):
                print("All checks passed. Valid gesture detected")
                self.valid_gesture_flag = True # Change state to True if all checks passed
                print(f"Valid gesture flag: {self.valid_gesture_flag}") # Debug: log Flag status change from False to True
                self.last_valid_time = time.time() # Store the time that all checks passed

                if self.detect_close_gesture(hand_landmark):
                    print("Close Window gesture detected. Closing Window...")  # Debug: log close window gesture
                    self.window_manager.close_frontmost_window()
                    return

                if self.detect_minimize_gesture(hand_landmark):
                    print("Minimize Window gesture detected. Minimizing Window...")  # Debug: log minimize window gesture
                    self.window_manager.minimize_frontmost_window()
                    return

                if self.detect_full_screen_gesture(hand_landmark):
                    print("Full Screen gesture detected. Entering Full Screen Window...")  # Debug: log enter full screen gesture
                    self.window_manager.full_screen_frontmost_window()
                    return
            else:
                print("Gesture checks failed")  # Debug: log gesture check failure
        else:
            print("No hand detected in the image")  # Debug: log when no hand is visible in webcam

        # Reset the flag if no valid gesture is detected for a certain time in seconds
        if self.valid_gesture_flag==True and (time.time() - self.last_valid_time > 1): # When flag is True and current time minus last valid time is greater than 1 second
            self.valid_gesture_flag = False # Reset flag to False so that a hand position check validation need to be executed again 
            print(f"Valid gesture flag: {self.valid_gesture_flag} (reset due to timeout)")  # Debug: log flag reset from True to False

    def detect_close_gesture(self, hand):
        thumb_tip = hand.landmark[4]
        pinky_tip = hand.landmark[20]
        # Calculate the distance between thumb and pinky tips
        distance_thumb_pinky = ((pinky_tip.x - thumb_tip.x) ** 2 + (pinky_tip.y - thumb_tip.y) ** 2) ** 0.5
        print("Distance between thumb and pinky:", distance_thumb_pinky)  # Debug: log distance between thumb and pinky
        return distance_thumb_pinky < 0.05  # Return True if the distance is below a threshold

    def detect_minimize_gesture(self, hand):
        thumb_tip = hand.landmark[4]
        ring_tip = hand.landmark[16]
        # Calculate the distance between thumb and ring tips
        distance_thumb_ring = ((ring_tip.x - thumb_tip.x) ** 2 + (ring_tip.y - thumb_tip.y) ** 2) ** 0.5
        print("Distance between thumb and ring:", distance_thumb_ring)  # Debug: log distance between thumb and ring
        return distance_thumb_ring < 0.05  # Return True if the distance is below a threshold

    def detect_full_screen_gesture(self, hand):
        thumb_tip = hand.landmark[4]
        middle_tip = hand.landmark[12]
        # Calculate the distance between thumb and middle tips
        distance_thumb_middle = ((middle_tip.x - thumb_tip.x) ** 2 + (middle_tip.y - thumb_tip.y) ** 2) ** 0.5
        print("Distance between thumb and middle:", distance_thumb_middle)  # Debug: log distance between thumb and middle
        return distance_thumb_middle < 0.05  # Return True if the distance is below a threshold
