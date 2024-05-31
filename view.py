# This module manages the display and user interface, interacting with the controller to reflect changes based on gestures

import cv2
from controller import GestureController
from model import HandDetector, WindowManager

# Initialize components
hand_detector = HandDetector()  # Instance of the HandDetector class for hand detection and gesture recognition
window_manager = WindowManager()  # Instance of the WindowManager class for managing windows
gesture_controller = GestureController(hand_detector, window_manager)  # Controller for handling gestures and interacting with the model and view

class GestureView:
    def __init__(self, gesture_controller):
        self.gesture_controller = gesture_controller # GestureController instance

    def display(self, image):
        print("Displaying image...") # Debug: log display function being called
        cv2.imshow("Hand gesture control", image)
        cv2.waitKey(10)  

def main():
    # Initialize components
    hand_detector = HandDetector()  # Instance of the HandDetector class for hand detection and gesture recognition
    window_manager = WindowManager()  # Instance of the WindowManager class for managing windows
    gesture_controller = GestureController(hand_detector, window_manager)  # Controller for handling gestures and interacting with the model and view

    # Open the webcam
    webcam = cv2.VideoCapture(0)  # Initialize the webcam (0 indicates the camera number)

    # Main loop to capture and process video frames
    while True:
        _, image = webcam.read()  # Read a frame from the webcam
        image = cv2.flip(image, 1)  # Flip the image horizontally for a mirror effect
        # using this width and height to identify the x and y. The underscore is the depth to provide an empty value of the same
        frame_height, frame_width, _ = image.shape
        gesture_controller.process_gestures(image)  # Process gestures using the controller
        cv2.imshow("Hand gesture control", image)  # Display the image with the hand gesture information

        key = cv2.waitKey(10)  # Wait for a key press for 10 milliseconds
        print(" 'Escape' key pressed:", key) # Debug: log when 'escape' key is pressed
        if key == 27:  # Check if the pressed key is the 'Escape' key (27)
            break

    # Release the webcam and close all windows
    webcam.release()  # Release the webcam resources
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()
