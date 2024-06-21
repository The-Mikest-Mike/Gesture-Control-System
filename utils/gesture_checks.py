# This module contains helper functions for additional landmark checks for hand gesture detection

import math

def additional_landmark_checks(hand):
    '''
    Checks if the thumb tip is positioned below or slightly above other fingertips
    by comparing the vertical position (y-coordinate) of the thumb tip landmark 
    with the vertical positions of the tips of the pinky, ring, and middle fingers
    
    Params:
        hand (mediapipe Hands.Hand): Detected hand object containing landmarks

    Returns:
        bool: True if the thumb tip is positioned below or up to a threshold above other fingertips, False otherwise
    '''
    pinky_tip = hand.landmark[20]  # Pinky tip landmark
    ring_tip = hand.landmark[16]   # Ring tip landmark
    middle_tip = hand.landmark[12] # Middle tip landmark
    thumb_tip = hand.landmark[4]   # Thumb tip landmark

    # Condition to ensure that the thumb is positioned below or slightly above other fingertips
    if thumb_tip.y < pinky_tip.y or thumb_tip.y < ring_tip.y or thumb_tip.y < middle_tip.y:
        return False
    return True

def pips_above_mcps(hand):
    '''
    Check if PIP landmarks are above MCP landmarks for index, middle, ring, and pinky fingers
    In MediaPipe's coordinate system, a lower y-value corresponds to a higher position in the image

    Params:
        hand (mediapipe Hands.Hand): Detected hand object containing landmarks

    Returns:
        bool: True if all PIP landmarks are positioned above MCP landmarks, False otherwise
    '''
    finger_pip_mcp_landmarks = {
        'index': (hand.landmark[6], hand.landmark[5]),  # Index PIP and MCP
        'middle': (hand.landmark[10], hand.landmark[9]),  # Middle PIP and MCP
        'ring': (hand.landmark[14], hand.landmark[13]),  # Ring PIP and MCP
        'pinky': (hand.landmark[18], hand.landmark[17])  # Pinky PIP and MCP
    }

    for finger, (pip, mcp) in finger_pip_mcp_landmarks.items():
        if pip.y >= mcp.y:
            print(f'{finger.capitalize()} PIP is below MCP. Ignoring gestures')  # Debug: log
            return False
    print("All PIP landmarks are above MCP landmarks")  # Debug: log
    return True

def calculate_angle(point1, point2, point3):
    '''
    Helper function to calculate the angle between three points

    Params:
        point1: The first point (landmark)
        point2: The second point (landmark)
        point3: The third point (landmark)

    Returns:
        float: The angle in degrees between the three points.
    '''
    a = (point1.x - point2.x)**2 + (point1.y - point2.y)**2
    b = (point3.x - point2.x)**2 + (point3.y - point2.y)**2
    c = (point1.x - point3.x)**2 + (point1.y - point3.y)**2

    cos_angle = (a + b - c) / (2 * math.sqrt(a) * math.sqrt(b))
    cos_angle = max(min(cos_angle, 1.0), -1.0)  # Ensure the cosine value is within the valid range [-1, 1]

    angle = math.degrees(math.acos(cos_angle))
    return angle

def hand_angle_validation(hand_landmarks):
    '''
    Validate hand angle to check if the palm is facing the camera and the middle finger is pointing up

    Params:
        hand_landmarks (mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList): Detected hand landmarks

    Returns:
        bool: True if the hand angle is valid, False otherwise
    '''
    wrist_landmark = hand_landmarks.landmark[0]  # Store wrist landmark
    middle_finger_pip_landmark = hand_landmarks.landmark[9]  # Store middle finger PIP landmark
    middle_finger_dip_landmark = hand_landmarks.landmark[10]  # Store middle finger DIP landmark
    middle_finger_tip_landmark = hand_landmarks.landmark[12]  # Store middle finger tip landmark
    thumb_cmc_landmark = hand_landmarks.landmark[1]  # Store thumb CMC landmark
    thumb_mcp_landmark = hand_landmarks.landmark[2]  # Store thumb MCP landmark
    thumb_ip_landmark = hand_landmarks.landmark[3]  # Store thumb IP landmark

    # Check if the wrist landmark is positioned below the middle finger tip landmark
    if wrist_landmark.y < middle_finger_tip_landmark.y:
        print("Invalid hand position. Wrist is above the middle finger tip")
        return False

    # Calculate the angle between the middle finger PIP, DIP, and tip landmarks
    middle_finger_angle = calculate_angle(
        middle_finger_pip_landmark,
        middle_finger_dip_landmark,
        middle_finger_tip_landmark
    )

    # Calculate the angle between the thumb CMC, MCP, and IP landmarks
    thumb_angle = calculate_angle(
        thumb_cmc_landmark,
        thumb_mcp_landmark,
        thumb_ip_landmark
    )

    print(f"Middle finger angle: {middle_finger_angle}")  # Debug: log middle finger angle value
    print(f"Thumb angle: {thumb_angle}")  # Debug: log thumb finger angle value

    middle_finger_angle_threshold = (150, 180)  # Middle finger pointing up extended <-> flexed
    thumb_angle_threshold = (160, 180)  # Thumb finger extended <-> flexed 
    
    # Check if the middle finger angle is within the valid range
    is_middle_finger_valid = middle_finger_angle_threshold[0] <= middle_finger_angle <= middle_finger_angle_threshold[1]
    # Check if the thumb finger angle is within the valid range
    is_thumb_valid = thumb_angle_threshold[0] <= thumb_angle <= thumb_angle_threshold[1]

    print(f"Middle finger valid: {is_middle_finger_valid}")  # Debug: log validation status
    print(f"Thumb valid: {is_thumb_valid}")  # Debug: log validation status

    middle_finger_aligned = (
        middle_finger_tip_landmark.y < middle_finger_dip_landmark.y < middle_finger_pip_landmark.y < wrist_landmark.y
    )
    print(f"Middle finger aligned: {middle_finger_aligned}")  # Debug: log alignment status

    return is_middle_finger_valid and is_thumb_valid and middle_finger_aligned
