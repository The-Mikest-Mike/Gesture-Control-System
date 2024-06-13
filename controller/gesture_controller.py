# Acts as an intermediary between the model and the view. It listens to the input from the view, 
# processes it (using the model if necessary) and updates the view accordingly
# Have methods that are called by the view to perform actions and update the model
# Components: GestureController

import mediapipe as mp
from utils.gesture_checks import additional_landmark_checks, pips_above_mcps

class GestureController:
    def __init__(self, hand_detector, window_manager):
        self.hand_detector = hand_detector  # Instance of HandDetector for detecting hands
        self.window_manager = window_manager  # Instance of WindowManager for managing windows
        self.drawing_utils = mp.solutions.drawing_utils  # Utility for drawing hand landmarks

    def process_gestures(self, image):
        print("Processing gestures...")  # Debug: log process_gestures function being called
        hand_landmark = self.hand_detector.detect_single_hand(image)  # Detect single hand in the provided image

        if hand_landmark:  # Check if a hand is detected
            print("Single hand detected")
            self.drawing_utils.draw_landmarks(image, hand_landmark, mp.solutions.hands.HAND_CONNECTIONS)  # Draw landmarks on detected hand in 'image' by using the 'drawing_utils' object

            if pips_above_mcps(hand_landmark):
                print("PIP check passed for all fingers")

                if additional_landmark_checks(hand_landmark):  # Check if thumb is positioned below all other fingertips
                    print("Thumb is below all other fingertips. Valid Hand Position")  # Debug: log whether thumb below other fingers

                    # Collect landmarks from the hand
                    thumb_tip = hand_landmark.landmark[4]  # Thumb tip landmark
                    pinky_tip = hand_landmark.landmark[20]  # Pinky tip landmark
                    ring_tip = hand_landmark.landmark[16]  # Ring tip landmark
                    middle_tip = hand_landmark.landmark[12]  # Middle tip landmark

                    # Calculate the distance between thumb and pinky tips
                    distance_thumb_pinky = ((pinky_tip.x - thumb_tip.x) ** 2 + (pinky_tip.y - thumb_tip.y) ** 2) ** 0.5
                    print("Distance between thumb and pinky:", distance_thumb_pinky)  # Debug: log distance between thumb and pinky

                    # Calculate the distance between thumb and ring tips
                    distance_thumb_ring = ((ring_tip.x - thumb_tip.x) ** 2 + (ring_tip.y - thumb_tip.y) ** 2) ** 0.5
                    print("Distance between thumb and ring:", distance_thumb_ring)  # Debug: log distance between thumb and ring

                    # Calculate the distance between thumb and middle tips
                    distance_thumb_middle = ((middle_tip.x - thumb_tip.x) ** 2 + (middle_tip.y - thumb_tip.y) ** 2) ** 0.5
                    print("Distance between thumb and middle:", distance_thumb_middle)  # Debug: log distance between thumb and middle

                    # Check for specific gestures and perform actions
                    # Close window gesture (thumb touching pinky fingertip)
                    if distance_thumb_pinky < 0.05:  # If distance below threshold, consider it "close window" gesture
                        print("Close Window gesture detected. Closing Window...")  # Debug: log valid threshold for close window gesture
                        self.window_manager.close_frontmost_window()
                        return

                    # Minimize window gesture (thumb touching ring fingertip)
                    if distance_thumb_ring < 0.05:  # If distance below threshold, consider it "minimize window" gesture
                        print("Minimize Window gesture detected. Minimizing Window...")  # Debug: log valid threshold for minimize window gesture
                        self.window_manager.minimize_frontmost_window()
                        return

                    # Full screen gesture (thumb touching middle fingertip)
                    if distance_thumb_middle < 0.05:  # If distance below threshold, consider it "full screen" gesture
                        print("Full Screen gesture detected. Entering Full Screen Window...")  # Debug: log valid threshold for enter full screen gesture
                        self.window_manager.full_screen_frontmost_window()
                        return

                    print("No valid gesture detected")  # Debug: log no valid gesture after above threshold conditions
                else:
                    print("Thumb is not below all other fingertips. Ignoring gestures")  # Debug: log invalid hand position
