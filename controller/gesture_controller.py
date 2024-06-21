# Acts as an intermediary between the model and the view. It listens to the input from the view, 
# processes it (using the model if necessary), and updates the view accordingly.
# Components: GestureController

import mediapipe as mp
from utils.gesture_checks import additional_landmark_checks, pips_above_mcps, hand_angle_validation
import time

class GestureController:
    def __init__(self, hand_detector, window_manager):
        self.hand_detector = hand_detector
        self.window_manager = window_manager
        self.drawing_utils = mp.solutions.drawing_utils
        self.valid_gesture_flag = False
        self.last_valid_time = None
        self.dragging = False
        self.previous_position = None
    
    def process_gestures(self, image):
        hand_landmark = self.hand_detector.detect_single_hand(image)
        if hand_landmark:
            self.drawing_utils.draw_landmarks(image, hand_landmark, mp.solutions.hands.HAND_CONNECTIONS)

            if self.valid_gesture_flag or (pips_above_mcps(hand_landmark) and additional_landmark_checks(hand_landmark) and hand_angle_validation(hand_landmark)):
                self.valid_gesture_flag = True
                self.last_valid_time = time.time()

                if self.detect_close_gesture(hand_landmark):
                    self.window_manager.close_frontmost_window()
                    return

                if self.detect_minimize_gesture(hand_landmark):
                    self.window_manager.minimize_frontmost_window()
                    return

                if self.detect_full_screen_gesture(hand_landmark):
                    self.window_manager.full_screen_frontmost_window()
                    return

                if self.detect_pickup_gesture(hand_landmark):
                    try:
                        self.window_manager.pickup_window()
                        self.dragging = True
                        self.previous_position = (hand_landmark.landmark[8].x, hand_landmark.landmark[8].y)
                        
                        self.detect_drag_gesture(hand_landmark)
                        self.window_manager.drag_window(hand_landmark)
                        
                    except Exception as e:
                        print(f"Error Dragging Window: {e}")
                        
                elif self.detect_drop_gesture(hand_landmark):
                        self.window_manager.drop_window()
                        self.dragging = False
                        return
            else:
                self.valid_gesture_flag = False
        else:
            self.valid_gesture_flag = False

        if self.valid_gesture_flag and (time.time() - self.last_valid_time > 1):
            self.valid_gesture_flag = False

    def calculate_landmarks_distance(self, point1, point2):
        return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.5

    def detect_close_gesture(self, hand):
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[20]) < 0.05

    def detect_minimize_gesture(self, hand):
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[16]) < 0.05

    def detect_full_screen_gesture(self, hand):
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[12]) < 0.05

    def detect_pickup_gesture(self, hand):
        print("Checking for pickup gesture...")
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[8]) < 0.05

    def detect_drag_gesture(self, hand):
        print("Checking for drag gesture...")
        return self.detect_pickup_gesture(hand)

    def detect_drop_gesture(self, hand):
        print("Checking for drop gesture...")
        return self.calculate_landmarks_distance(hand.landmark[4], hand.landmark[8]) > 0.1
