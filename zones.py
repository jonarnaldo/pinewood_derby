import cv2

def get_motion_zone():
    cap = cv2.VideoCapture(0)
    selected_roi = None

    print("Step 1: Press 's' to select your motion zone.")
    print("Step 2: After drawing, press ENTER.")
    print("Step 3: Press 'q' to finish and return coordinates.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Setup", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            # This returns (x, y, w, h)
            selected_roi = cv2.selectROI("Setup", frame, fromCenter=False)
            cv2.destroyWindow("ROI selector") # Clean up selector window
            print(f"Zone captured: {selected_roi}")
            
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return selected_roi

# Execute and capture the values
motion_zone = get_motion_zone()

if motion_zone and motion_zone[2] > 0:
    x, y, w, h = motion_zone
    print(f"\n--- Configuration Saved ---")
    print(f"X-Coordinate: {x}")
    print(f"Y-Coordinate: {y}")
    print(f"Width:        {w}")
    print(f"Height:       {h}")
else:
    print("No zone was selected.")