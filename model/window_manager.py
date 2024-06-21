# Manages the data logic and interactions with the data
# Components: WindowManager

import pyautogui
from AppKit import NSWorkspace, NSRunningApplication
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import time

class WindowManager:
    def __init__(self):
        self.dragging = False  # Initialize dragging state to False

    def get_active_window_info(self):
        '''
        Retrieves information about the currently active window
        
        Returns:
            dict: Information about the active window if found, else None
        '''
        options = kCGWindowListOptionOnScreenOnly  # Option to list only on-screen windows
        window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)  # Retrieve the list of all on-screen windows
        active_application = NSWorkspace.sharedWorkspace().frontmostApplication()  # Get the currently active (frontmost) application
        active_application_pid = active_application.processIdentifier()  # Get the process identifier (PID) of the active application

        for window in window_list:
            if window['kCGWindowOwnerPID'] == active_application_pid and window['kCGWindowLayer'] == 0:
                return window # Return the active window if it matches the PID and is at layer 0
        return None # Return None if no matching window is found

    def pickup_window(self):
        '''
        Initiates the action to pick up (click and hold) the frontmost window for dragging
        '''
        try:
            window_info = self.get_active_window_info()  # Retrieve information about the active window
            if not window_info:
                return  # Exit if no active window information is available

            window_left_edge = window_info['kCGWindowBounds']['X']  # Get the X coordinate of the window's left edge
            window_top_edge = window_info['kCGWindowBounds']['Y']  # Get the Y coordinate of the window's top edge
            window_width = window_info['kCGWindowBounds']['Width']  # Get the width of the window

            estimated_title_bar_height = 22  # Estimate for the height of the window title bar
            center_x_of_window = window_left_edge + window_width // 2  # Calculate the X coordinate of the window's center
            title_bar_center_y = window_top_edge + estimated_title_bar_height // 2  # Calculate the Y coordinate of the title bar's center

            pyautogui.moveTo(center_x_of_window, title_bar_center_y)  # Move the mouse to the calculated center of the title bar
            time.sleep(0.1)  # Brief pause to ensure the move action completes
            pyautogui.mouseDown()  # Simulate mouse down action to pick up the window
            print("Mouse down click")  # Debug: Log mouse down action
            self.dragging = True  # Set dragging state to True
            print(f"Dragging state {self.dragging}")  # Debug: Log dragging state
        except Exception as e:
            print(f"Error Picking Up Window: {e}") # Debug: Log any error that occurs during pickup a window

    def drag_window(self, hand_landmark):
        '''
        Drags the window based on the movement of the hand landmark.
        
        Args:
            hand_landmark: The detected hand landmarks used to calculate the new window position.
        '''
        screen_width, screen_height = pyautogui.size()
        index_finger_tip = hand_landmark.landmark[8]
        try:
            if index_finger_tip is not None:
                x = int(index_finger_tip.x * screen_width)
                y = int(index_finger_tip.y * screen_height)
                pyautogui.moveTo(x, y)
                print("Dragging window")  # Debug: Log dragging window action
        except Exception as e:
            print(f"Error Dragging Window: {e}") # Debug: Log any error that occurs during dragging a window

    def drop_window(self):
        '''
        Releases the click to drop the window at the current position
        '''
        try:
            pyautogui.mouseUp() # Simulate mouse up action to drop the window
            print("Mouse up release click")  # Debug: Log mouse up action
            self.dragging = False  # Reset dragging state
            print(f"Dragging state {self.dragging}")  # Debug: Logs dragging state false
        except Exception as e:
            print(f"Error Dropping Window: {e}") # Debug: Log any error that occurs during dropping a window

    def minimize_frontmost_window(self):
        '''
        Minimizes the frontmost window
        '''
        try:
            active_application = NSWorkspace.sharedWorkspace().frontmostApplication() # Get the currently active (frontmost) application
            if not active_application:
                return # Exit if there is no active application
            application_reference = NSRunningApplication.runningApplicationWithProcessIdentifier_(active_application.processIdentifier()) # Get a reference to the active application using its process identifier (PID)
            application_reference.hide() # Hide (minimize) the active application
        except Exception as e:
            print(f"Error Minimizing Window: {e}") # Debug: Log any error that occurs during minimization

    def close_frontmost_window(self):
        '''
        Closes the frontmost window
        '''
        try:
            pyautogui.hotkey('command', 'w') # Simulate pressing 'command + w' to close the window
        except Exception as e:
            print(f"Error Closing Window: {e}") # Debug: Log any error that occurs during window closing

    def full_screen_frontmost_window(self):
        '''
        Toggles the frontmost window to full screen
        '''
        try:
            pyautogui.hotkey('fn', 'f') # Simulate pressing 'fn + f' to toggle full screen mode
        except Exception as e:
            print(f"Error Entering Full Screen: {e}") # Debug: Log any error that occurs during full screen toggle
