import cv2
import Handtracking as ht
import time
import autopy
import numpy as np
import threading

######## Variable Initialization ###############
prevTime=0
curTime=0

delay=3
prevX,prevY=0,0
curX,curY=0,0

specLength=15
mDown=False
mUp=True
######## Video Capture Box #####################
camHeight=400
camWidth=640
screenWidth, screenHeight=autopy.screen.size()
frameReduction=100
cap=cv2.VideoCapture(1)
cap.set(3,camWidth)
cap.set(4,camHeight)

####### Class Intialization #############
detector=ht.HandTracking(model_complexity=1,min_detection_confidence=0.9,min_tracking_confidence=0.3)

########## Main Program ################
while True:
    ret,frame=cap.read()
    # Locate Hand Landmarks And Draw
    displayFrame=detector.locateHands(frame, draw=True)
    list=detector.findLandmarks(frame, inputHandType = "Right", draw=True) #This function also makes sure that only the chosen hand is used for the mouse movement
    # Check If Hand Is Detected On Screen
    if len(list) !=0:
        # Determine Which Fingers Are Extended/Closed
        fingers=detector.fingerCounter()
        # Borders for Mouse Movement
        cv2.rectangle(frame, (frameReduction,frameReduction),(camWidth-frameReduction,camHeight-frameReduction),(255,255,255),2)
        # Determine The Coordinate of Index Finger
        [iX,iY]=list[detector.fingerTips[1]][1:]
        # Convert Coordinates In Relation To Monitor
        sX=np.interp(iX,(frameReduction,camWidth-frameReduction),(0,screenWidth))
        sY=np.interp(iY,(frameReduction,camHeight-frameReduction),(0,screenHeight))
        # Every Finger Except for Index Is Closed: Mouse Move Mode
        if fingers[0]==0 and fingers[2]==0:
            # If statement to prevent out of bounds error
            if (screenWidth-sX)<screenWidth and sY<screenHeight:
                # Move The Mouse
                autopy.mouse.move(screenWidth-sX,sY)
            cv2.circle(frame, (iX, iY), 5, (0, 255, 0), cv2.FILLED)
        # Index Finger And Thumb Extended: Click Mode
        if fingers[0]==1 and fingers[2]==0:
            curX,curY=autopy.mouse.location()
            # Determine Distance Between Fingers 
            length=detector.distBetweenFingers(frame, list[detector.fingerTips[0]], list[detector.fingerTips[1]], draw=True,specLength=specLength)
            # Click The Mouse if They are Close
            if length<specLength:
                if mDown==False:
                   autopy.mouse.toggle(down=True)
                   mDown=True
                   mUp=False
                   start_time = time.time()
                if time.time()-start_time>1.5:
                    # If statement to prevent out of bounds error
                    if (screenWidth-sX)<screenWidth and sY<screenHeight:
                        # Move The Mouse
                        autopy.mouse.move(screenWidth-sX,sY)
            if length>specLength: 
                if mUp==False:
                    autopy.mouse.toggle(down=False)
                    mDown=False
                    mUp=True     
    #10. Calculate FPS
    curTime=time.time()
    fps=1/(curTime-prevTime)
    prevTime=curTime
    cv2.putText(frame,str(int(fps)),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    #11. Display
    cv2.imshow("Display Box", displayFrame)
    cv2.waitKey(1)