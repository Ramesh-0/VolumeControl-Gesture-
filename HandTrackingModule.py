import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw = True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

    def fingersUp(self, img):
        lmList = self.findPosition(img, draw=False)  # Get landmark list

        if len(lmList) == 0:
            return []  # Return empty list if no hand detected

        fingers = []
        tipIds = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

        # Detect if it's a left or right hand
        isLeftHand = lmList[5][1] > lmList[17][1]  # Index base (5) vs pinky base (17)

        # Improved Thumb detection using distance
        thumbTipX, thumbTipY = lmList[tipIds[0]][1], lmList[tipIds[0]][2]  # Thumb tip
        thumbBaseX, thumbBaseY = lmList[tipIds[0] - 2][1], lmList[tipIds[0] - 2][2]  # Thumb base

        thumbDistance = abs(thumbTipX - thumbBaseX)  # Distance in X direction

        # If thumb is far enough from its base, it's considered "up"
        if thumbDistance > 40:  # Adjust threshold if needed
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers (move vertically)
        for i in range(1, 5):
            if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:
                fingers.append(1)  # Finger is up
            else:
                fingers.append(0)  # Finger is down

        return fingers  # Returns a list like [1, 1, 0, 0, 0] (Only thumb & index up)


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)  # Use default webcam
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    detector = handDetector()
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image. Exiting...")
            break  # Exit the loop if frame capture fails
        img= detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close OpenCV windows

if __name__== "__main__" :
    main()