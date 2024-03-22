import pyautogui
import mediapipe as mp
from gesture_checks import additional_landmark_checks # Import additional landmark checks function

class GestureController:
    def __init__(self, hand_detector, window_manager):
        # Initialize instances
        self.hand_detector = hand_detector
        self.window_manager = window_manager
        self.drawing_utils = mp.solutions.drawing_utils  # To draw things in hands

    def process_gestures(self, image):
        print("Processing gestures...")  # Debugging Line only. Notify when this function is called
        # Process gestures based on detected hands in the provided image
        hands = self.hand_detector.detect_hands(image)
        if hands:
            for hand in hands:
                # Draw the landmarks for the hands in 'image' by using the 'drawing_utils' object
                self.drawing_utils.draw_landmarks(image, hand)

                # Check if thumb is positioned below all other fingertips
                if additional_landmark_checks(hand):
                    print("Thumb is below all other fingertips. Performing associated action...")

                    # Collect all the landmarks from the hand
                    landmarks = hand.landmark
                    # Detecting a "close window" gesture based on the proximity of thumb tip and pinky tip landmarks
                    thumb_tip = hand.landmark[4]  # Thumb tip landmark
                    pinky_tip = hand.landmark[20]  # Pinky tip landmark

                    # Detecting a "minimize window" gesture based on the proximity of thumb tip and ring tip landmarks
                    thumb_tip = hand.landmark[4]  # Thumb tip landmark
                    ring_tip = hand.landmark[16]  # Ring tip landmark

                    # Detecting a "full screen window" gesture based on the proximity of thumb tip and middle tip landmarks
                    thumb_tip = hand.landmark[4]  # Thumb tip landmark
                    middle_tip = hand.landmark[12]  # Middle tip landmark

                    # Calculate the distance between thumb and pinky tips
                    distance_thumb_pinky = ((pinky_tip.x - thumb_tip.x) ** 2 + (pinky_tip.y - thumb_tip.y) ** 2) ** 0.5
                    print("Distance between thumb and pinky:", distance_thumb_pinky)  # Debugging Line only. Informs when this function is called and the distance value.

                    # Calculate the distance between thumb and ring tips
                    distance_thumb_ring = ((ring_tip.x - thumb_tip.x) ** 2 + (ring_tip.y - thumb_tip.y) ** 2) ** 0.5
                    print("Distance between thumb and ring:", distance_thumb_ring)  # Debugging Line only. Informs when this function is called and the distance value.

                    # Calculate the distance between thumb and middle tips
                    distance_thumb_middle = ((middle_tip.x - thumb_tip.x) ** 2 + (middle_tip.y - thumb_tip.y) ** 2) ** 0.5
                    print("Distance between thumb and middle:", distance_thumb_ring)  # Debugging Line only. Informs when this function is called and the distance value.

                    # Check for close gesture (thumb touching pinky fingertip)
                    if distance_thumb_pinky < 0.05:  # If distance below threshold, consider it "close window" gesture
                        print("Close Window gesture detected. Closing Window...")
                        self.window_manager.close_frontmost_window()
                        break

                    # Calling "detect_close_gesture" function
                    if self.hand_detector.detect_close_gesture(hand):
                        print("Close Window gesture detected. Closing Window...")
                        self.window_manager.close_frontmost_window()
                        break

                    # Check for minimize gesture (thumb touching ring fingertip)
                    if distance_thumb_ring < 0.05:  # If distance below threshold, consider it "minimize window" gesture
                        print("Minimize Window gesture detected. Minimizing Window...")
                        self.window_manager.minimize_frontmost_window()
                        break

                    # Calling "detect_minimize_gesture" function
                    if self.hand_detector.detect_minimize_gesture(hand):
                        print("Minimize Window gesture detected. Minimizing Window...")
                        # Implement the action to minimize the window (you may need to find the appropriate API for this)
                        break

                    # Check for full screen gesture (thumb touching middle fingertip)
                    if distance_thumb_middle < 0.05:  # If distance below threshold, consider it "full screen" gesture
                        print("Full Screen gesture detected. Entering Full Screen Window...")
                        self.window_manager.full_screen_frontmost_window()
                        break

                    # Calling "detect_full_screen_gesture" function
                    if self.hand_detector.detect_full_screen_gesture(hand):
                        print("Full Screen gesture detected. Entering Full Screen Window...")
                        self.window_manager.full_screen_frontmost_window()
                        break

                    # When no gesture detected, print message
                    else:
                        print("No valid gesture detected")
                    
                else:
                    print("Thumb is not below all other fingertips. Ignoring gestures.")


