## Description

This app uses motion sensing via openCV and a phone camera to determine finish line winner for a Pinewood Derby. It is recommended to use a camera with at least 60fps in order to capture accurate finish line placement.

## Development

activate env

```
source race_env/bin/activate
```

install dependencies

```
pip install -r requirements.txt
```

save setup

```
pip freeze > requirements.txt
```

define zone

```
python3 zones.py
```

update zone, then run main

```
python3 main.py
```

## Using Mobile phone

you will need to install scrcpy if using phone as a camera. scrcpy is a free, open-source tool that lets you display and control your Android device from your computer — over USB or Wi-Fi. In this case, we will be using USB to reduce latency.

1. Install scrcpy

```
brew install scrcpy
```

2. Make sure Transferring files / Aundroid Auto is selected in USB settings. Then, run this Bash command

```
scrcpy --video-source=camera --camera-id=0 --camera-fps=60 --camera-size=1920x1080 --video-bit-rate=16M --no-audio --video-buffer=0
```

3. Run OBS and start virtual camera
   1. Add a new Source
      1. Select Method: Window Capture
      2. Select Window: [Scrcpy][some phone model]
   2. Click "Start Virtual Camera"

4. In a separate Terminal window (not in VS code) run this command to start motion detection:

```
python3 main.py
```

## Troubleshooting

you may need to install adb

```
brew install --cask android-platform-tools
```

Critical Hardware Tip for Samsung A35
Before you run the command, ensure your phone is set to Motion Smoothness: High.

Go to Settings > Display.

Tap Motion Smoothness.

Select Adaptive (120Hz) and hit Apply.

While this is a display setting, it often unlocks the higher frame rate pipelines for the camera and OS, ensuring the USB port isn't capped at 30 FPS.

Best Practice for the Finish Line
Side-on Angle: Don't point the camera straight at the cars' front. Point it across the track (perpendicular). This makes it much easier for computer vision to see exactly when the "nose" of the car breaks the plane of the finish line.

Tape a Reference Line: Put a thin piece of high-contrast tape (like bright green or blue) exactly on the finish line. In your CV code, you only need to monitor the pixels on that line.
