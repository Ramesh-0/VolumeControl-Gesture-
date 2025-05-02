import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#############################
wCam, hCam = 640, 480
#############################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Reads system volume
currentVolume = volume.GetMasterVolumeLevelScalar()  # Returns volume in range 0.0 to 1.0
volPercentage = int(currentVolume * 100)  # Convert to percentage
volBar = np.interp(currentVolume, [0.0, 1.0], [450, 150])  # Scale according to the system volume

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detection_confidence=0.7)
vol = 0
length = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Center of the line

        cv2.circle(img, (x1, y1), 10, (0, 128, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 128, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (0, 128, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 128, 255), 3)

        fingers = detector.fingersUp(img)  # Returns a list [1,1,1,1,1] if all fingers are up

        if fingers == [1, 1, 1, 1, 1]:  # If all fingers are up, stop adjusting volume
            cv2.putText(img, "Volume Control Paused", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            length = math.hypot(x2 - x1, y2 - y1)

            if length < 20:
                cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

            # Convert hand range (20-160) to volume range (-63 to 0)
            vol = np.interp(length, [20, 160], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)  # Set system volume

            # Get updated system volume percentage
            currentVolume = volume.GetMasterVolumeLevelScalar()  # Get volume in range 0.0 - 1.0
            volPercentage = int(currentVolume * 100)  # Convert to percentage
            volBar = np.interp(currentVolume, [0.0, 1.0], [450, 150])  # Scale bar

    # Draw Volume Bar UI
    cv2.rectangle(img, (50, 150), (100, 450), (200, 200, 200), cv2.FILLED)  # Background
    cv2.rectangle(img, (50, 150), (100, 450), (50, 50, 50), 3)  # Border
    cv2.rectangle(img, (50, int(volBar)), (100, 450), (0, 122, 255), cv2.FILLED)  # Volume Level

    # Display numerical volume percentage
    cv2.putText(img, f"{volPercentage}%", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)

    # FPS Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close OpenCV windows
