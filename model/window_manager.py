# Manages the data logic and interactions with the data
# Components: WindowManager
import pyautogui
from AppKit import NSWorkspace, NSRunningApplication
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import time

class WindowManager:
    def __init__(self):
        self.dragging = False

    def get_active_window_info(self):
        options = kCGWindowListOptionOnScreenOnly
        window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        active_application = NSWorkspace.sharedWorkspace().frontmostApplication()
        active_application_pid = active_application.processIdentifier()

        for window in window_list:
            if window['kCGWindowOwnerPID'] == active_application_pid and window['kCGWindowLayer'] == 0:
                return window
        return None

    def pickup_window(self):
        try:
            window_info = self.get_active_window_info()
            if not window_info:
                return

            window_left_edge = window_info['kCGWindowBounds']['X']
            window_top_edge = window_info['kCGWindowBounds']['Y']
            window_width = window_info['kCGWindowBounds']['Width']

            estimated_title_bar_height = 22
            center_x_of_window = window_left_edge + window_width // 2
            title_bar_center_y = window_top_edge + estimated_title_bar_height // 2

            pyautogui.moveTo(center_x_of_window, title_bar_center_y)
            time.sleep(0.1)
            pyautogui.mouseDown()
            print("Mouse down click") # Debug: Log mouse down action
            self.dragging = True
            print(f"Dragging state {self.dragging}") # Debug: Log dragging state
        except Exception as e:
            print(f"Error Picking Up Window: {e}")

    def drag_window(self, hand_landmark):
        screen_width, screen_height = pyautogui.size()
        index_finger_tip = hand_landmark.landmark[8]
        try:
            if index_finger_tip is not None:
                x = int(index_finger_tip.x * screen_width)
                y = int(index_finger_tip.y * screen_height)
                pyautogui.moveTo(x, y)
                print("Dragging window") # Debug: Log dragging window action
        except Exception as e:
            print(f"Error Dragging Window: {e}")

    def drop_window(self):
        try:
            pyautogui.mouseUp()
            print("Mouse up release click") # Debug: Log mouse up action
            self.dragging = False
            print(f"Dragging state {self.dragging}") # Debug: Logs dragging state false
        except Exception as e:
            print(f"Error Dropping Window: {e}")

    def minimize_frontmost_window(self):
        try:
            active_application = NSWorkspace.sharedWorkspace().frontmostApplication()
            if not active_application:
                return
            application_reference = NSRunningApplication.runningApplicationWithProcessIdentifier_(active_application.processIdentifier())
            application_reference.hide()
        except Exception as e:
            print(f"Error Minimizing Window: {e}")

    def close_frontmost_window(self):
        try:
            pyautogui.hotkey('command', 'w')
        except Exception as e:
            print(f"Error Closing Window: {e}")

    def full_screen_frontmost_window(self):
        try:
            pyautogui.hotkey('fn', 'f')
        except Exception as e:
            print(f"Error Entering Full Screen: {e}")
