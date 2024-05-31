# initializes and runs the components for hand gesture recognition and control

from view import GestureView, WindowManager 
from model import HandDetector
from controller import GestureController
import cv2

# Create instances of model, view, and controller classes
hand_detector = HandDetector() # Hand detctor instance from model.py
window_manager = WindowManager() # Window manager instance from view.py
gesture_controller = GestureController(hand_detector, window_manager) # Gesture controller instance from controller.py
gesture_view = GestureView(gesture_controller)  # GestureView instance from view.py

# Open the webcam
webcam = cv2.VideoCapture(0)

# Main loop to capture and process video frames
while True:
    _, image = webcam.read() # Read a frame from webcam
    image = cv2.flip(image, 1) # Flip the image horizontally for a mirror effect
    print("Processing new frame. . .") # Debug: log when a frame is processed
    gesture_controller.process_gestures(image) # Process gestures using the controller
    cv2.imshow("Hand gesture control",image) # Display the image with hand gesture information

    key = cv2.waitKey(10) # Wait for a key press for 10 miliseconds
    print(" 'Escape' key pressed:", key) # Debug: log 'escape' key being pressed
    if key == 27: # Check if the pressed key is the 'Escape' key (27)
        break # Exit the loop if 'Escape' key is pressed

