from model.hand_detector import HandDetector
from model.window_manager import WindowManager
from controller.gesture_controller import GestureController
from view.main_view import MainView
import cv2

# Initialize instances
hand_detector = HandDetector()  # Hand detector instance from model/hand_detector.py
window_manager = WindowManager()  # Window manager instance from model/window_manager.py
gesture_controller = GestureController(hand_detector, window_manager)  # Gesture controller instance from controller/gesture_controller.py
main_view = MainView(hand_detector, window_manager, gesture_controller)  # Main view instance from view/main_view.py

# Initializes the webcam
webcam = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = webcam.read()  # Capture a frame from the webcam (ret: return boolean value, frame: actual frame captured from webcam)
        if not ret:  # If capturing the frame fails
            print("Failed to capture image. Exiting...")  # Debug: log failure
            break
        
        frame = cv2.flip(frame, 1)  # Flip the image horizontally for a mirror effect
        print("Processing new frame...")  # Debug: log frame processing
        
        gesture_controller.process_gestures(frame)  # Process gestures using the controller
        main_view.display_frame(frame)  # Display the frame with hand gesture information

        key = cv2.waitKey(10)  # Wait for a key press for 10 milliseconds
        if key == 27:  # Check if the pressed key is the 'Escape' key (27)
            print("'Escape' key pressed. Exiting...")  # Debug: log when 'Escape' key is pressed
            break  # Exit the loop if 'Escape' key is pressed

finally:
    webcam.release()  # Release the webcam resources
    cv2.destroyAllWindows()  # Close all OpenCV windows
    print("Webcam and OpenCV windows closed.")  # Debug: log resource cleanup
