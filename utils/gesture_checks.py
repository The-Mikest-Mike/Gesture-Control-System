# This module contains helper fuctions for additional landmark checks for hand gesture detection
import math

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
    finger_pip_mcp_landmarks = {
        'index': (hand.landmark[6], hand.landmark[5]),  # Index PIP and MCP
        'middle': (hand.landmark[10], hand.landmark[9]),  # Middle PIP and MCP
        'ring': (hand.landmark[14], hand.landmark[13]),  # Ring PIP and MCP
        'pinky': (hand.landmark[18], hand.landmark[17])  # Pinky PIP and MCP
    }

    # Iterate through each finger, comparing if the PIP landmark is above the MCP landmark (has a smaller y-coordinate)
    for finger, (pip, mcp) in finger_pip_mcp_landmarks.items():
        if pip.y >= mcp.y:
            print(f'{finger} pip.y index {pip.y} >= mcp.y index {mcp.y}')  # Debug: log
            print(f"{finger.capitalize()} PIP is below MCP. Ignoring gestures")
            return False # If any PIP landmark is not above their corresponding MCP landmark
        print("All PIP landmars are above MCP landmarks")
        return True # If all PIP landmarks are above their corresponding MCP landmark
    
def calculate_angle(point1, point2, point3):
    """
    Helper function to calculate the angle between three points.

    Params:
        point1: The first point (landmark).
        point2: The second point (landmark).
        point3: The third point (landmark).

    Returns:
        float: The angle in degrees between the three points.
    """
    # Calculate the squared distances between the points
    a = (point1.x - point2.x)**2 + (point1.y - point2.y)**2
    b = (point3.x - point2.x)**2 + (point3.y - point2.y)**2
    c = (point1.x - point3.x)**2 + (point1.y - point3.y)**2

    # Calculate the cosine of the angle using the cosine rule
    cos_angle = (a + b - c) / (2 * math.sqrt(a) * math.sqrt(b))
    
    # Ensure the cosine value is within the valid range [-1, 1]
    cos_angle = max(min(cos_angle, 1.0), -1.0)

    # Calculate the angle in degrees
    angle = math.degrees(math.acos(cos_angle))
    return angle

def hand_angle_validation(hand_landmarks):
    """
    Validate hand angle to check if the palm is facing the camera and middle finger is pointing up.

    Params:
        hand_landmarks (mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList): Detected hand landmarks

    Returns:
        bool: True if the hand angle is valid, False otherwise
    """
    # Define landmarks for the middle finger and wrist
    wrist_landmark = hand_landmarks.landmark[0]
    middle_finger_pip_landmark = hand_landmarks.landmark[9]
    middle_finger_dip_landmark = hand_landmarks.landmark[10]
    middle_finger_tip_landmark = hand_landmarks.landmark[12]

    # Define landmarks for the thumb finger
    thumb_cmc_landmark = hand_landmarks.landmark[1]
    thumb_mcp_landmark = hand_landmarks.landmark[2]
    thumb_ip_landmark = hand_landmarks.landmark[3]

    # Check if wrist is lower than the middle finger tip (inverted y-axis)
    if wrist_landmark.y < middle_finger_tip_landmark.y:
        print("Invalid hand position. Wrist is above the middle finger tip")
        return False

    # Calculate the angle of the middle and thumb finger
    middle_finger_angle = calculate_angle(
        middle_finger_pip_landmark,
        middle_finger_dip_landmark,
        middle_finger_tip_landmark
    )

    thumb_angle = calculate_angle(
        thumb_cmc_landmark,
        thumb_mcp_landmark,
        thumb_ip_landmark
    )

    print(f"Middle finger angle: {middle_finger_angle}") # Debug: log middle finger angle value
    print(f"Thumb angle: {thumb_angle}") # Debug: log thumb finger angle value

    # Define the threshold ranges for valid angles (fixed values)
    middle_finger_angle_threshold = (150, 180)  # Middle finger pointing up extended <-> flexed
    thumb_angle_threshold = (160, 180)  # Thumb finger extended <-> flexed 

    # Check if the angles are within the threshold
    # [0] refers to the first position (the lower bound for middle finger angle)
    # [1] refers to the second position (the upper bound for middle finger angle)
    is_middle_finger_valid = middle_finger_angle_threshold[0] <= middle_finger_angle <= middle_finger_angle_threshold[1] 
    is_thumb_valid = thumb_angle_threshold[0] <= thumb_angle <= thumb_angle_threshold[1]

    print(f"Middle finger valid: {is_middle_finger_valid}") # Debug: False if fail the validation, else True
    print(f"Thumb valid: {is_thumb_valid}") # Debug: False if fail the validation, else True

    # Ensure the middle finger landmarks are vertically aligned
    # [0] refers to the first position (the lower bound for thumb angle)
    # [1] refers to the second position (the upper bound for thumb angle)
    middle_finger_aligned = (
        middle_finger_tip_landmark.y < middle_finger_dip_landmark.y < middle_finger_pip_landmark.y < wrist_landmark.y
    )
    print(f"Middle finger aligned: {middle_finger_aligned}") # Debug: False if fail the validation, else True

    return is_middle_finger_valid and is_thumb_valid and middle_finger_aligned


