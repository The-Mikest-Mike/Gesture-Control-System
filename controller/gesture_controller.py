# Acts as an intermediary between the model and the view. It listens to the input from the view, 
# processes it (using the model if necessary), and updates the view accordingly.
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
        self.dragging = False  # Initialize dragging flag as false
        self.previous_position = None  # Initialize previous position
    
    def process_gestures(self, image):
        '''Processes the gestures detected in the image'''
        hand_landmark = self.hand_detector.detect_single_hand(image)
        # Draw landmarks on detected hand in 'image' by using the 'drawing_utils' object
        if hand_landmark:
            print("Hand detected")  # Debug: log when a hand is detected
            self.drawing_utils.draw_landmarks(image, hand_landmark, mp.solutions.hands.HAND_CONNECTIONS)

            if self.valid_gesture_flag or (
                pips_above_mcps(hand_landmark) and 
                additional_landmark_checks(hand_landmark) and 
                hand_angle_validation(hand_landmark)
            ):
                self.valid_gesture_flag = True  # Change state to True if all checks passed
                print(f"Valid gesture flag: {self.valid_gesture_flag}")  # Debug: log Flag status change from False to True
                self.last_valid_time = time.time()  # Store the time that all checks passed

                # Detect and handle close gesture
                if self.detect_close_gesture(hand_landmark):
                    self.window_manager.close_frontmost_window()
                    return

                # Detect and handle minimize gesture
                if self.detect_minimize_gesture(hand_landmark):
                    self.window_manager.minimize_frontmost_window()
                    return

                # Detect and handle full screen gesture
                if self.detect_full_screen_gesture(hand_landmark):
                    self.window_manager.full_screen_frontmost_window()
                    return

                # Detect and handle pickup gesture
                if self.detect_pickup_gesture(hand_landmark):
                    try:
                        self.window_manager.pickup_window()
                        self.dragging = True  # Set dragging flag to true
                        self.previous_position = (hand_landmark.landmark[8].x, hand_landmark.landmark[8].y)
                        
                        self.detect_drag_gesture(hand_landmark)  # Check for drag gesture
                        self.window_manager.drag_window(hand_landmark)
                        
                    except Exception as e:
                        print(f"Error Dragging Window: {e}")  # Debug: log any error during dragging
                        
                # Detect and handle drop gesture
                elif self.detect_drop_gesture(hand_landmark):
                    self.window_manager.drop_window()
                    self.dragging = False  # Reset dragging flag
                    return
            else:
                self.valid_gesture_flag = False  # Reset flag if validation checks fail
        else:
            self.valid_gesture_flag = False  # Reset flag if no hand is detected

        # Reset the flag if no valid gesture is detected for a certain time in seconds
        if self.valid_gesture_flag and (time.time() - self.last_valid_time > 1):  # When flag is True and current time minus last valid time is greater than 1 second
            self.valid_gesture_flag = False  # Reset flag to False so that a hand position check validation need to be executed again 
            print(f"Valid gesture flag: {self.valid_gesture_flag} (reset due to timeout)")  # Debug: log flag reset from True to False

    def calculate_landmarks_distance(self, point1, point2):
        '''Calculates the distance between two landmarks'''
        return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.5

    def detect_close_gesture(self, hand):
        '''Detects the gesture to close the frontmost window'''
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[20]) < 0.05  # Return True if the distance is below a threshold

    def detect_minimize_gesture(self, hand):
        '''Detects the gesture to minimize the frontmost window'''
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[16]) < 0.05  # Return True if the distance is below a threshold

    def detect_full_screen_gesture(self, hand):
        '''Detects the gesture to make the frontmost window full screen'''
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[12]) < 0.05  # Return True if the distance is below a threshold

    def detect_pickup_gesture(self, hand):
        '''Detects the gesture to pick up a window'''
        print("Checking for pickup gesture...")
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[8]) < 0.05  # Return True if the distance is below a threshold

    def detect_drag_gesture(self, hand):
        '''Detects the gesture to drag a window'''
        print("Checking for drag gesture...")
        return self.detect_pickup_gesture(hand)  # Reuse pickup gesture detection for dragging

    def detect_drop_gesture(self, hand):
        '''Detects the gesture to drop a window'''
        print("Checking for drop gesture...")
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[8]) > 0.1  # Return True if the distance is above a threshold
