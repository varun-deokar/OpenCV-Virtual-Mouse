import cv2
import autopy
import numpy as np
import HandTrackingModule as htm
import time

# Output and Live Screen Dimensions
wCam, hCam = 640, 480
wScr, hScr = autopy.screen.size()

c = 0  # Counter variable to check number of clicks
pTime = 0
lmList = []
box_reduction_width = 100  # Pixels to pad output area

smoothening = 7  # Number of pixel increments to reduce shakiness
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Setting up Video through Web Cam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialising object of handDetector class
detector = htm.handDetector(detectionCon=0.7, trackCon=0.7, maxHands=1)

while True:
    success, img = cap.read()

    # Detecting Hand
    img = detector.findHands(img, draw=True)

    # Finding co-ordinates of hand
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Finding co-ordinates of index finger

        fingers = detector.fingersUp()  # Getting info about which fingers are up
        cv2.rectangle(img, (box_reduction_width, 30), (wCam - box_reduction_width, hCam//2 + 50),
                      (255, 0, 255), 2)

        # Moving the cursor
        if fingers[1] == 1 and fingers[2] == 0 and fingers[4] == 0:
            c = 0
            x3 = np.interp(x1, (box_reduction_width, wCam - box_reduction_width), (0, wScr))
            y3 = np.interp(y1, (30, hCam//2 + 50), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)

            plocX, plocY = clocX, clocY

        # Single CLick
        if fingers[1] == 1 and fingers[2] == 1:
            # length, img, _ = detector.findDistance(8, 12, img)
            # if length < 40:
            if c == 0:
                autopy.mouse.click()
                c += 1

        # Double Click
        if fingers[1] == 1 and fingers[4] == 1:
            # length, img, _ = detector.findDistance(8, 12, img)
            # if length < 40:
            if c == 0 or c == 1:
                autopy.mouse.click()
                c += 1

    # Frame Rate Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f"FPS {int(fps)}", (15, hCam - 50), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 0, 255), 2)

    # Output
    cv2.imshow('Output', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
