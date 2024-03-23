# gesture_checks.py

def additional_landmark_checks(hand):
    """
    Checks if thumb tip is positioned below or slightly above other fingertips
    by comparing the vertical position (y-coordinate) of the thumb tip landmark 
    with the vertical positions of the tips of the pinky, ring, and middle fingers. 
    
    Params:
        hand (mediapipe Hands.Hand): Detected hand object containing landmarks.

    Returns:
        bool: True if the thumb tip is positioned below or up to 0.05 (threshold) above other fingertips, False otherwise.
    """
    # Define the threshold for the thumb to be considered slightly above other fingertips
    #threshold = 0.01

    pinky_tip = hand.landmark[20]  # Pinky tip landmark
    ring_tip = hand.landmark[16]   # Ring tip landmark
    middle_tip = hand.landmark[12] # Middle tip Landmark
    thumb_tip = hand.landmark[4]   # Thumb tip landmark

    # Compare the y-coordinates of thumb tip with y-coordinates of tips of the pinky, ring, and middle fingers.
    # Condition to ensure that the thumb is positioned below or up to 0.01 above other fingertips
    if thumb_tip.y < pinky_tip.y or thumb_tip.y < ring_tip.y or thumb_tip.y < middle_tip.y:
        print("Thumb is not below all other fingertips. Ignoring gestures.")
        return False
    else:
        return True
