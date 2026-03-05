import os
import time
import cv2

def draw_live_meter(frame, m1, t1, m2, t2):
    """Shows motion levels for both lanes."""
    cv2.rectangle(frame, (10, 10), (350, 90), (0,0,0), -1)
    # Lane 1 Status
    c1 = (0,0,255) if m1 > t1 else (0,255,0)
    cv2.putText(frame, f"L1 Pixels: {m1}/{t1}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, c1, 2)
    # Lane 2 Status
    c2 = (0,0,255) if m2 > t2 else (0,255,0)
    cv2.putText(frame, f"L2 Pixels: {m2}/{t2}", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, c2, 2)

def monitor_zone():
    """monitors two lanes."""
    cap = cv2.VideoCapture(2) # Changed back to 0 for testing; adjust as needed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # --- CALIBRATION SETTINGS ---
    motion_threshold = 80
    sensitivity = 0.03

    # Define two separate zones (x, y, w, h)
    # Adjust these so one box is over Lane 1 and the other over Lane 2
    lane1_geo = (816, 65, 192, 141) 
    lane2_geo = (851, 288, 239, 145)

    # Thresholds
    t1 = int((lane1_geo[2] * lane1_geo[3]) * sensitivity)
    t2 = int((lane2_geo[2] * lane2_geo[3]) * sensitivity)

    ret, first_frame = cap.read()
    if not ret: return

    folder = "race_results"
    if not os.path.exists(folder):
        os.makedirs(folder)

    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    # Initial ROIs
    x1, y1, w1, h1 = lane1_geo
    x2, y2, w2, h2 = lane2_geo
    roi1_ref = first_gray[y1:y1+h1, x1:x1+w1]
    roi2_ref = first_gray[y2:y2+h2, x2:x2+w2]

    # Winner Tracking
    l1_time = None
    l2_time = None
    winner_declared = False

    while True:
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Process Lane 1
        roi1 = gray[y1:y1+h1, x1:x1+w1]
        diff1 = cv2.absdiff(roi1_ref, roi1)
        _, thresh1 = cv2.threshold(diff1, motion_threshold, 255, cv2.THRESH_BINARY)
        m1 = cv2.countNonZero(thresh1)

        # Process Lane 2
        roi2 = gray[y2:y2+h2, x2:x2+w2]
        diff2 = cv2.absdiff(roi2_ref, roi2)
        _, thresh2 = cv2.threshold(diff2, motion_threshold, 255, cv2.THRESH_BINARY)
        m2 = cv2.countNonZero(thresh2)

        now = time.time()

        # Detection Logic
        if m1 > t1 and l1_time is None:
            l1_time = now
            if l2_time is None:
                cv2.putText(frame, "WINNER: LANE 1", (x1, y1 - 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
            
            filename = f"L1_Finish_{time.strftime('%H%M%S')}.jpg"
            cv2.imwrite(os.path.join(folder, filename), frame)
            print("Captured Lane 1 Finish!")

        if m2 > t2 and l2_time is None:
            l2_time = now
            # If Lane 1 hasn't finished yet, Lane 2 is the winner
            if l1_time is None:
                cv2.putText(frame, "WINNER: LANE 2", (x2, y2 - 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

            filename = f"L2_Finish_{time.strftime('%H%M%S')}.jpg"
            cv2.imwrite(os.path.join(folder, filename), frame)
            print("Captured Lane 2 Finish!")

        # Winner UI logic
        if l1_time and l2_time and not winner_declared:
            diff = abs(l1_time - l2_time)
            winner = "Lane 1" if l1_time < l2_time else "Lane 2"
            print(f"WINNER: {winner} by {diff:.4f} seconds!")
            winner_declared = True

        # Draw UI
        draw_live_meter(frame, m1, t1, m2, t2)
        cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0,255,0), 2)
        cv2.putText(frame, "L1", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.rectangle(frame, (x2, y2), (x2+w2, y2+h2), (0,255,0), 2)
        cv2.putText(frame, "L2", (x2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if winner_declared:
            msg = f"WINNER: {'L1' if l1_time < l2_time else 'L2'} (+{abs(l1_time-l2_time):.3f}s)"
            cv2.putText(frame, msg, (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

        cv2.imshow("Race Monitor", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('r'):
            l1_time = l2_time = None
            winner_declared = False
            # Reset references
            ret, f = cap.read()
            first_gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            roi1_ref = first_gray[y1:y1+h1, x1:x1+w1]
            roi2_ref = first_gray[y2:y2+h2, x2:x2+w2]

    cap.release()
    cv2.destroyAllWindows()

monitor_zone()
