# Initializes and runs the components for hand gesture recognition and control.

from model.hand_detector import HandDetector
from model.window_manager import WindowManager
from controller.gesture_controller import GestureController
from view.main_view import MainView
import cv2

# Initialize instances
hand_detector = HandDetector()  # Hand detector instance from model.py
window_manager = WindowManager()  # Window manager instance from model.py
gesture_controller = GestureController(hand_detector, window_manager)  # Gesture controller instance from controller.py
main_view = MainView() # Main view instance from  view.py

# Open the webcam
webcam = cv2.VideoCapture(0)

# Main loop to capture and process video frames
while True:
    _, image = webcam.read()  # Read a frame from the webcam
    image = cv2.flip(image, 1)  # Flip the image horizontally for a mirror effect
    print("Processing new frame...")  # Debug: log
    gesture_controller.process_gestures(image)  # Process gestures using the controller
    main_view.display(image) # Display the image with hand gesture information

    key = cv2.waitKey(10)  # Wait for a key press for 10 milliseconds
    if key == 27:  # Check if the pressed key is the 'Escape' key (27)
        print("'Escape' key pressed:", key)  # Debug: log when 'escape' key is pressed
        break  # Exit the loop if 'Escape' key is pressed

# Release the webcam and close all windows
webcam.release()  # Release the webcam resources
cv2.destroyAllWindows()  # Close all OpenCV windows
