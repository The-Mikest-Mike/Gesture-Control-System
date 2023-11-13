# import needed libraries
import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time

# Function to close the frontmost window
def close_frontmost_window():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        active_window.close()

# creating 4 variables initializing them with 0.
x1 = y1 = x2 = y2 = 0
# open our webcam. Number 0 means 1 camera. It stands for the number of cameras.
webcam = cv2.VideoCapture(0) 

# creating object2
my_hands = mp.solutions.hands.Hands() # to capture our hands
drawing_utils = mp.solutions.drawing_utils # to draw things in our hands

# show the captured image in a window.
while True:
    _, image = webcam.read() 
    # fipling the image to mirror our cam and properly identify the fingers. (0 means 'x' axis, 1 means 'y' axis)
    image = cv2.flip(image, 1)
    # using this width and height to identify the x and y. The underscore is the depth to provide an empty value of the same
    frame_height, frame_width, _ = image.shape
    # convert the image from BGR to rgb
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # we are passing our 'image' 
    # variable to process the hand, giving it the rgb_image
    output = my_hands.process(rgb_image)

    # Check if hands are detected
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            # draw the landmarks of the hands in 'image' by using the '.drawing_utils' object.
            drawing_utils.draw_landmarks(image, hand)
            # collect all the landmarks from the hand
            landmarks = hand.landmark

            # Detecting a "close full hand" gesture based on the proximity of certain landmarks (e.g., thumb and pinky)
            thumb_tip = hand.landmark[4]  # Thumb tip landmark
            pinky_tip = hand.landmark[20]  # Pinky tip landmark

            # Calculate the distance between thumb and pinky tips
            distance_thumb_pinky = ((pinky_tip.x - thumb_tip.x) ** 2 + (pinky_tip.y - thumb_tip.y) ** 2) ** 0.5

            # If the distance is below a certain threshold, consider it a "close full hand" gesture
            if distance_thumb_pinky < 0.05:  # Adjust the threshold as needed
                print("Closed full hand gesture detected. Closing Window...")
                close_frontmost_window()
                break

            #time.sleep(1)  # Introduce a delay to avoid rapid adjustments but it causes delay

    cv2.imshow("Hand gesture control", image) # show the captured image in a window.
    key = cv2.waitKey(10) # this will wait for 10 ms and then repeat the while loop to ensure continuous capturing.


# Release webcam and close all windows
webcam.release()
cv2.destroyAllWindows()