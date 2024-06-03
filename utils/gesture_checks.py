# This module contains helper fuctions for additional landmark checks for hand gesture detection

def additional_landmark_checks(hand):
    """
    Checks if thumb tip is positioned below or slightly above other fingertips
    by comparing the vertical position (y-coordinate) of the thumb tip landmark 
    with the vertical positions of the tips of the pinky, ring, and middle fingers. 
    
    Params:
        hand (mediapipe Hands.Hand): Detected hand object containing landmarks.

    Returns:
        bool: True if the thumb tip is positioned below or up to threshold above other fingertips, False otherwise.
    """
   
    pinky_tip = hand.landmark[20]  # Pinky tip landmark
    ring_tip = hand.landmark[16]   # Ring tip landmark
    middle_tip = hand.landmark[12] # Middle tip Landmark
    thumb_tip = hand.landmark[4]   # Thumb tip landmark

    # Condition to ensure that the thumb is positioned above other fingertips
    if thumb_tip.y < pinky_tip.y or thumb_tip.y < ring_tip.y or thumb_tip.y < middle_tip.y:
        print("Thumb is not below all other fingertips. Ignoring gestures.") # Debug: log when thumb is not below other fingers
        return False
    else:
        return True
