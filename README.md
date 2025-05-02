
# Volume Control with Hand Gestures

This project allows you to control your system volume using hand gestures detected by your webcam, specifically by measuring the distance between your thumb and index finger. It also provides a reusable HandTrackingModule that you can integrate into your own Python projects for custom hand-tracking applications.




## Features

- Real-time hand landmark detection using [MediaPipe](https://developers.google.com/mediapipe)
- Smooth system volume adjustment using pycaw
- Modular design — use HandTrackingModule.py separately in other projects
- Simple webcam interface with visual feedback (OpenCV window)


## Installation

- Clone this repository:
```bash
  git clone https://github.com/Ramesh-0/VolumeControl-Gesture.git
```
- Navigate into the folder:
```bash
  cd VolumeControl-Gesture
```
- Install required Python packages:
```bash
  pip install -r requirements.txt
```
## Usage
Run the main script:
```bash
  python volumeHandControl.py
```
- Show your hand in front of the webcam.
- Move your thumb and index finger closer or farther to adjust the volume.
- Raise all fingers to pause volume control.
- Press q to quit the application

## Requirements
- Python 3.x
- Webcam
- Windows OS (required for pycaw to control system audio)
## Demo

https://github.com/user-attachments/assets/5356b03f-2867-4ce2-9d19-3ae6d6fb078e


## Acknowledgements

 - [MediaPipe](https://developers.google.com/mediapipe) by Google
 - [PyCaw](https://github.com/AndreMiras/pycaw)
 - [OpenCV](https://opencv.org)

Feel free to fork this project and use the HandTrackingModule for your own creative applications!
