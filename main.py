"""Module providing opencv library with Live Calibration Meter."""
import os
import time
import cv2

def monitor_zone():
    print("Race Monitor Active...")
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FPS, 60)

    print("Initializing camera...")
    # 1. Check if the hardware/stream is even accessible
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    folder = "race_results"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # --- CALIBRATION SETTINGS ---
    MOTION_THRESHOLD = 80 # Color change sensitivity
    SENSITIVITY_PERCENT = 0.03 # 3% of the zone must change to trigger
    motion_zone = (946, 83, 271, 179) # (x, y, w, h)
    x, y, w, h = motion_zone

    # Calculate the actual pixel threshold based on zone size
    AREA_THRESHOLD = int((w * h) * SENSITIVITY_PERCENT)

    ret, first_frame = cap.read()
    if not ret:
        print("Camera Error")
        exit()

    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_roi = first_gray[y:y+h, x:x+w]
    has_triggered = False

    while True:
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = gray[y:y+h, x:x+w]

        frame_delta = cv2.absdiff(first_roi, roi)
        _, thresh = cv2.threshold(frame_delta, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)
        motion_count = cv2.countNonZero(thresh)

        # --- UI & VISUAL FEEDBACK ---
        color = (0, 0, 255) if motion_count > AREA_THRESHOLD else (0, 255, 0)
        
        # 1. Draw the Live Meter (top left)
        cv2.rectangle(frame, (10, 10), (300, 60), (0,0,0), -1) # Black background for text
        cv2.putText(frame, f"Pixels: {motion_count}", (20, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Goal: >{AREA_THRESHOLD} (3%)", (20, 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # 2. Draw the Motion Zone
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Trigger Logic
        if motion_count > AREA_THRESHOLD:
            if not has_triggered:
                timestamp = time.strftime("%H%M%S")
                cv2.imwrite(os.path.join(folder, f"finish_{timestamp}.jpg"), frame)
                print(f"TRIPPED! Motion: {motion_count}")
                # has_triggered = True

        cv2.imshow("Race Feed - Press 'r' to Reset", frame)
        cv2.imshow("Delta View", thresh)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            ret, first_frame = cap.read()
            first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
            first_roi = first_gray[y:y+h, x:x+w]
            has_triggered = False

    cap.release()
    cv2.destroyAllWindows()


monitor_zone()