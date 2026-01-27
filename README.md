## Description

This app uses motion sensing via openCV and a webcam to determine finish line winner for a Pinewood Derby

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

Install scrcpy

```
brew install scrcpy
```

run this Bash command

```
scrcpy --video-source=camera --camera-id=0 --camera-fps=60 --camera-size=1920x1080 --video-bit-rate=16M --no-audio --video-buffer=0
```

Run OBS and start virtual camera

In a separate Terminal window (not in VS code) run this command to start motion detection:

```
python3 main.py
```

## Troubleshooting

you may need to install adb

```
brew install --cask android-platform-tools
```

Critical Hardware Tip for A35
Before you run the command, ensure your phone is set to Motion Smoothness: High.

Go to Settings > Display.

Tap Motion Smoothness.

Select Adaptive (120Hz) and hit Apply.

While this is a display setting, it often unlocks the higher frame rate pipelines for the camera and OS, ensuring the USB port isn't capped at 30 FPS.

Best Practice for the Finish Line
Side-on Angle: Don't point the camera straight at the cars' front. Point it across the track (perpendicular). This makes it much easier for computer vision to see exactly when the "nose" of the car breaks the plane of the finish line.

Tape a Reference Line: Put a thin piece of high-contrast tape (like bright green or blue) exactly on the finish line. In your CV code, you only need to monitor the pixels on that line.
