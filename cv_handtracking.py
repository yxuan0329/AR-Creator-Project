# -*- coding: utf-8 -*-
import numpy as np
import cv2
import keyboard
import math
from cvzone.HandTrackingModule import HandDetector


class Btn: # the UI button
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 30
        self.color = (0, 255, 255)
        
    def draw(self, background):
        cv2.ellipse(background, (self.x, self.y), (self.radius, self.radius), 0, 0, 360, self.color, -1)

class FingerTip: # the position of the finger tip (thumb, index_finger, middle_finger, ring_finger, pinky)
    def __init__(self, x, y):
        self.x = x
        self.y = y

# parameter
WIDTH, HEIGHT = 640, 360 # 1280, 720
selection = -1
select_mode = -1
counter = 0


btn0 = Btn(120, 50)
btn1 = Btn(200, 50)
btn2 = Btn(280, 50)
btn3 = Btn(360, 50)
btn_list = [btn0, btn1, btn2, btn3]

def drawUI(img):
    for btn in btn_list:
        btn.draw(img)
    

def get_frame(cap):
    success, img = cap.read() # get the frame from webcam
    fingers = [0,0,0,0,0]
    hands, img = detector.findHands(img)
    
    drawUI(img)
    
    data = []
    lmList = []
    
    # landmark values - (x, y, z) * 21
    for hand in hands:        
        lmList = hand['lmList']
        for lm in lmList:
            data.extend([lm[0], lm[1], lm[2]]) # reverse y-dir
                
        fingers = detector.fingersUp(hand) # [1, 1, 1, 1, 1] if fingers up
        print(fingers)
        # print(len(data))
        detect_click_btn(img, data, fingers)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

def distance(a, b):
    dis = pow((a.x - b.x), 2) + pow(a.y - b.y, 2)
    dis = math.sqrt(dis)
    return dis

def detect_click_btn(img, data, fingers):
    global selection, select_mode, counter
    counterspeed = 8
    index_finger_tip = FingerTip(int(data[24]), int(data[25]))

    if fingers == [0, 1, 0, 0, 0] and distance(index_finger_tip, btn_list[0]) <= btn_list[0].radius: 
        if selection != 0: # ENTER SELECTION 0
            counter = 1
        selection = 0
        # print("selection = 0")
    elif fingers == [0, 1, 0, 0, 0] and distance(index_finger_tip, btn_list[1]) <= btn_list[1].radius :
        if selection != 1: # ENTER SELECTION 1
            counter = 1
        selection = 1
        # print("selection = 1")
    elif fingers == [0, 1, 0, 0, 0] and distance(index_finger_tip, btn_list[2]) <= btn_list[2].radius : 
        if selection != 2: # ENTER SELECTION 2
            counter = 1
        selection = 2
        # print("selection = 2")
    elif fingers == [0, 1, 0, 0, 0] and distance(index_finger_tip, btn_list[3]) <= btn_list[3].radius : 
        if selection != 3: # ENTER SELECTION 3
            counter = 1
        selection = 3
        # print("selection = 3")
    else: # QUIT SELECTON
        selection = -1
        counter = 0
        # print("quit selection")
        
    if counter > 0: 
        counter += 1
        print (counter, selection)
        cv2.ellipse(img, (btn_list[selection].x, btn_list[selection].y), (btn_list[selection].radius, btn_list[selection].radius), 0, 0, counter * counterspeed, (0, 255, 0), 10)
        if counter * counterspeed >= 360:
            select_mode = selection
            print ("enter mode " + str(selection))
            counter = 0
            selection = -1
            



if __name__ == '__main__':
    cap = cv2.VideoCapture(0) # device number = 0
    cap.set(3, WIDTH) # width 
    cap.set(4, HEIGHT) # height
    
    detector = HandDetector(maxHands=2, detectionCon=0.8) # hand detect
    selection = -1

    while True:
        get_frame(cap)
        
    
    cv2.destroyAllWindows()
