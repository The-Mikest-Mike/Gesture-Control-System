import pyautogui
import mediapipe as mp

class GestureController:
    def __init__(self, hand_detector, window_manager):
        # Initialize instances
        self.hand_detector = hand_detector
        self.window_manager = window_manager
        self.drawing_utils = mp.solutions.drawing_utils  # to draw things in hands

    def process_gestures(self, image):
        print("Processing gestures...")  # Debugging Line only. Notify when this function is called
        # Process gestures based on detected hands in the provided image
        hands = self.hand_detector.detect_hands(image)
        if hands:
            for hand in hands:
                # Draw the landmarks for the hands in 'image' by using the 'drawing_utils' object
                self.drawing_utils.draw_landmarks(image, hand)

                # Collect all the landmarks from the hand
                landmarks = hand.landmark
                # Detecting a "close full hand" gesture based on the proximity of thumb and pinky landmarks
                thumb_tip = hand.landmark[4]  # Thumb tip landmark
                pinky_tip = hand.landmark[20]  # Pinky tip landmark

                # Calculate the distance between thumb and pinky tips
                distance_thumb_pinky = ((pinky_tip.x - thumb_tip.x) ** 2 + (pinky_tip.y - thumb_tip.y) ** 2) ** 0.5
                print("Distance between thumb and pinky:", distance_thumb_pinky)  # Debugging Line only. Informs when this function is called and the distance value.

                # Check for a specific gesture (e.g., closed full hand) using the hand_detector
                if distance_thumb_pinky < 0.05:  # If distance below threshold, consider it "close full hand" gesture
                    print("Closed full hand gesture detected. Closing Window...")
                    self.window_manager.close_frontmost_window()
                    break

                if self.hand_detector.detect_close_gesture(hand):
                    print("Closed full hand gesture detected. Closing Window...")
                    self.window_manager.close_frontmost_window()
                    break
