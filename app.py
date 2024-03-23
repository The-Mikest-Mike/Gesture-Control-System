# initializes and runs the components.
# gesture_app.py interacts with View.py, which, in turn, interacts with controller.py and model.py. 
# The GestureController in controller.py communicates with the HandDetector in model.py to process gestures.

from view import GestureView, WindowManager 
from model import HandDetector
from controller import GestureController
import cv2

# The classes are: GestureController, GestureView. Create instances of model, view and controller
hand_detector = HandDetector()
window_manager = WindowManager()
gesture_controller = GestureController(hand_detector, window_manager)
gesture_view = GestureView(gesture_controller)  # GestureView is a class defined in view.py

# Open the webcam
webcam = cv2.VideoCapture(0)

# Main loop to capture and process video frames
while True:
    _, image = webcam.read()
    image = cv2.flip(image, 1)
    print("Processing new frame. . .") # Debugging Line only. 
    gesture_controller.process_gestures(image)
    cv2.imshow("Hand gesture control",image)

    key = cv2.waitKey(10)
    print(" 'Escape' key pressed:", key)
    if key == 27:
        break

