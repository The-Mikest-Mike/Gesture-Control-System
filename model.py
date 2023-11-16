# Houses the HandDetector class, handling hand detection and gesture recognition.
import cv2
import pyautogui
import mediapipe as mp

# Handle hand detection and gesture recognition
class HandDetector:
    def __init__(self):
        # Initialize the mediapipe hands module
        self.hands = mp.solutions.hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils
        # creating 4 variables initializing them with 0.
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def detect_hands(self, image):
        print("Detecting hands. . .") # Debugging Line Only. Notify when this function is called
        # Use computer vision CV and the Mediapipe library to detect hands in the provided image.
        # Convert the image from BRG to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the image using mediapipe hands
        output = self.hands.process(rgb_image)
        # Get the detected hands
        hands = output.multi_hand_landmarks
        # Ensure that 'detect_hands' returns a list instead of 'None' to avoid " 'NoneType' object is not iterable" error
        return hands if hands is not None else []


    def detect_close_gesture(self, hand):
        print("Detecting close gesture. . .") # Debugging Line Only. Notify when this function is called
        # Implementation for detecting if the pinky finger is in contact with the thumb (close gesture)
        # Return a boolean indicating whether the minimize gesture is detected
        pass

    def detect_minimize_gesture(self, hand):
        print("Detecting minimize gesture. . .") # Debugging Line Only. Notify when this function is called
        # Implemention logic to detect if the ring finger is in contact with the thumb (minimize gesture)
        # Return a boolean indicating whether the minimize gesture is detected
        pass

class WindowManager:
    def __init__(self):
        # Initialize any necessary attributes
        pass

    def close_frontmost_window(self):
        # Implement window closing logic for macOS using pyautogui (I can use a specific library or system command)
        try:
            pyautogui.hotkey('command', 'w') # Simulate Command + w to close the frontmost window.
        except Exception as e:
            print(f"Error Closing Window: {e}")

    def minimize_frontmost_window(self):
        # Implement window minimizing logic for macOS (you may need to find the appropriate API for this)
        try:
            pyautogui.hotkey('command', 'm') # Simulate Command + m to minimize the frontmost window.
        except Exception as e:
            print(f"Exception Minimizing Window: {e}")
        pass


