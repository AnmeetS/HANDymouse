import cv2
import mediapipe as mp
import math

######## Hand Landmark Detection ###############
class HandTracking():
    def __init__(self,
               static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        # Setting Parameters to default values
        self.mode = static_image_mode
        self.maxH = max_num_hands
        self.complexity = model_complexity
        self.detcon = min_detection_confidence
        self.trackcon = min_tracking_confidence
        # Initializing the mediapipe hand landmarks detector
        self.mediapipeHand = mp.solutions.hands
        self.hand= self.mediapipeHand.Hands(self.mode,
                                            self.maxH,
                                            self.complexity,
                                            self.detcon,
                                            self.trackcon)
        # Initializing the mediapipe drawing utilities
        self.mediapipeDraw = mp.solutions.drawing_utils
        self.fingerTips = [4, 8, 12, 16, 20]
        self.internalList=[]
    def locateHands(self,frame,draw=False):
        #convert the frame from BGR color (which OpenCV uses) to RGB color (which mediapipe uses)
        RGBFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #Gather the hand landmarks
        self.data=self.hand.process(RGBFrame)
        #Draw the hand landmarks on the frame if detected
        if self.data.multi_hand_landmarks:
            for handLMS in self.data.multi_hand_landmarks:
                self.mediapipeDraw.draw_landmarks(frame,handLMS,self.mediapipeHand.HAND_CONNECTIONS)
        return frame
    def detHandType(self, flipType=True):
        # Default Value of The Hand Type
        handType ="Nothing"
        if self.data.multi_hand_landmarks:
            handInfo=self.data.multi_handedness
            # Used to flip the left and right hands since mediapipe assumes the image has not been flipped
            if flipType:
                if handInfo[0].classification[0].label=="Right":
                    handType ="Left"
                if handInfo[0].classification[0].label=="Left":
                    handType ="Right"
        return handType    
    def findLandmarks(self, frame, inputHandType = "Right", draw=False):
        # Initialzing the list of landmarks
        list=[]
        if self.data.multi_hand_landmarks:
            hand=self.data.multi_hand_landmarks[0]
            # Determining whether the hand on screen is the right or the left hand
            mphandSide=self.detHandType(flipType=True)
            if mphandSide == inputHandType:
                for fingerNumber, lm in enumerate (hand.landmark):
                    # Inputing the landmark coordinates into the list
                    height, width, channels = frame.shape
                    cx, cy = int(lm.x * width), int(lm.y * height)
                    list.append([fingerNumber, cx, cy])
                    # Drawing Blue Circles on each of the landmarks on the corresponding hand
                    if draw:
                        cv2.circle(frame, (cx, cy), 5, (255, 0 , 0), cv2.FILLED)
            else:
                cv2.putText(frame,str("REMOVE LEFT HAND"),(200,200),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2,cv2.LINE_AA)
        self.internalList=list
        return list
    def distBetweenFingers(self, frame, finger1, finger2, draw=False, line=False,specLength=0):
        #Grabbing the coordinates of the two landmarks referenced
        x1,y1=finger1[1],finger1[2]
        x2,y2=finger2[1],finger2[2]
        deltaX=x2-x1
        deltaY=y2-y1
        length = math.hypot(deltaX,deltaY)
        
        # Drawing Purple Circles on each of the landmarks and connecting them with a line
        if draw:
            cv2.circle(frame, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
            if length<specLength:
                cv2.circle(frame, (x1, y1), 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 5, (0, 255, 0), cv2.FILLED)
        if line:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 15)
        return length
    def fingerCounter(self):
        fingers=[]
        if self.data.multi_hand_landmarks:
            #Determine whether right or left hand is displayed  
            handType=self.detHandType(flipType=True)     
            # Determine whether the Thumb is Extended
            if handType == "Right":
                if self.internalList[self.fingerTips[0]][1] > self.internalList[self.fingerTips[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else: 
                if self.internalList[self.fingerTips[0]][1] < self.internalList[self.fingerTips[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # Determine whether the Index, Middle, Ring and Pinky Fingers are extended
            for id in range(1, 5):
                if self.internalList[self.fingerTips[id]][2] < self.internalList[self.fingerTips[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers