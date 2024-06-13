# This module contains helper fuctions for additional landmark checks for hand gesture detection

def additional_landmark_checks(hand):
    '''
    Checks if thumb tip is positioned below or slightly above other fingertips
    by comparing the vertical position (y-coordinate) of the thumb tip landmark 
    with the vertical positions of the tips of the pinky, ring, and middle fingers
    
    Params:
        hand (mediapipe Hands.Hand): Detected hand object containing landmarks

    Returns:
        bool: True if the thumb tip is positioned below or up to threshold above other fingertips, False otherwise
    '''
   
    pinky_tip = hand.landmark[20]  # Pinky tip landmark
    ring_tip = hand.landmark[16]   # Ring tip landmark
    middle_tip = hand.landmark[12] # Middle tip Landmark
    thumb_tip = hand.landmark[4]   # Thumb tip landmark

    # Condition to ensure that the thumb is positioned above other fingertips
    if thumb_tip.y < pinky_tip.y or thumb_tip.y < ring_tip.y or thumb_tip.y < middle_tip.y:
        return False
    else:
        return True


def pips_above_mcps(hand):
    '''
    Check if pip.y is less than mcp.y for index, middle, ring, and pinky fingers
    to determine if the PIP landmarks are above the MCP landmarks.
    In MediaPipe's coordinate system, the origin (0, 0) is at the top-left corner of the image,
    and the y-coordinates increase as you move down the image. Therefore, a lower y-value 
    corresponds to a higher position in the image, and a higher y-value corresponds to a lower position.

    Params:
        hand (mediapipe Hand.hand): Detected hand object containing landmarks

    Returns:
        bool: True if all PIP landmarks are positioned above MCP landmarks, False otherwise
    '''
    
    # Dictionary to store pip with their corresponding mcp landmarks
    finger_landmarks = {
        'index': (hand.landmark[6], hand.landmark[5]),  # Index PIP and MCP
        'middle': (hand.landmark[10], hand.landmark[9]),  # Middle PIP and MCP
        'ring': (hand.landmark[14], hand.landmark[13]),  # Ring PIP and MCP
        'pinky': (hand.landmark[18], hand.landmark[17])  # Pinky PIP and MCP
    }

    # Iterate through each finger, comparing if the PIP landmark is above the MCP landmark (has a smaller y-coordinate)
    for finger, (pip, mcp) in finger_landmarks.items():
        if pip.y >= mcp.y:
            print(f'{finger} pip.y index {pip.y} >= mcp.y index {mcp.y}')  # Debug: log
            print(f"{finger.capitalize()} PIP is below MCP. Ignoring gestures")
            return False # If any PIP landmark is not above their corresponding MCP landmark
        print("All PIP landmars are above MCP landmarks. Valid Hand Position")
        return True # If all PIP landmarks are above their corresponding MCP landmark