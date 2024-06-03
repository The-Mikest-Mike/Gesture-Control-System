# Displays the data from the model, captures user's input and
# sends user commands to the controller to reflect actions based on their gestures
# Components: Methods for displaying video feed and drawing landmarks

import cv2

class MainView:
    def __init__(self):
        pass

    def display(self, image):
        '''Display the image with hand gesture information'''
        cv2.imshow("Hand gesture control", image)
