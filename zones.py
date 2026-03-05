import cv2

def run_calibration():
    # Camera Setup (Change index if needed)
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    ret, frame = cap.read()
    if not ret:
        print("\n[!] ERROR: Could not access camera.")
        return

    print("\n" + "="*40)
    print("      PINEWOOD DERBY CALIBRATOR")
    print("="*40)
    print("INSTRUCTIONS:")
    print("1. Drag a box over LANE 1, then press ENTER.")
    print("2. Drag a box over LANE 2, then press ENTER.")
    print("3. Once both are drawn, press ESC.")
    print("="*40)

    # Select ROIs
    rects = cv2.selectROIs("Calibration Tool", frame, fromCenter=False)
    cv2.destroyAllWindows()
    cap.release()

    if len(rects) < 2:
        print("\n[!] SETUP FAILED: You didn't select enough lanes.")
        return

    # --- HUMAN READABLE OUTPUT ---
    print("\n✅ CALIBRATION COMPLETE\n")
    
    for i, r in enumerate(rects[:2], 1):
        x, y, w, h = r
        print(f"LANE {i} COORDINATES:")
        print(f"  • Top-Left:  ({x}, {y})")
        print(f"  • Dimensions: {w}px wide x {h}px high")
        print(f"  • Center:     ({x + w//2}, {y + h//2})")
        print("-" * 30)

    # --- CODE BLOCK OUTPUT ---
    print("\nPASTE THIS INTO YOUR MAIN SCRIPT:\n")
    print(f"lane1_geo = ({rects[0][0]}, {rects[0][1]}, {rects[0][2]}, {rects[0][3]})")
    print(f"lane2_geo = ({rects[1][0]}, {rects[1][1]}, {rects[1][2]}, {rects[1][3]})")
    print("\n" + "="*40)

if __name__ == "__main__":
    run_calibration()