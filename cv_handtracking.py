# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 20:23:34 2022

@author: xuan
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
# import socket

# parameter
WIDTH, HEIGHT = 640, 360 # 1280, 720
selection = -1
    


def get_frame(cap):
    # get the frame from webcam
    success, img = cap.read()
    fingers = [0,0,0,0,0]
    # hands
    hands, img = detector.findHands(img)
    
    data = []
    lmList = []
    
    # landmark values - (x, y, z) * 21
    #if hands:
    for hand in hands:        
        lmList = hand['lmList']
        for lm in lmList:
            data.extend([lm[0], HEIGHT - lm[1], lm[2]]) # reverse y-dir
                
        fingers = detector.fingersUp(hand) # [1, 1, 1, 1, 1] if fingers up
        print(fingers)
    # print(len(data))
    # sock.sendto(str.encode(str(data)), serverAddressPort)
        
    showUI(img)
    click_btn(fingers, img, selection)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

def showUI(img):
    cv2.ellipse(img, (80, 50), (20, 20), 0, 0, 360, (0, 255, 255), -1)
    cv2.ellipse(img, (80, 110), (20, 20), 0, 0, 360, (0, 255, 255), -1)
    cv2.ellipse(img, (80, 170), (20, 20), 0, 0, 360, (0, 255, 255), -1)
    cv2.ellipse(img, (80, 230), (20, 20), 0, 0, 360, (0, 255, 255), -1)

def click_btn(fingers, img, selection):
    if fingers == [0, 1, 0, 0, 0]:
        if selection != 1:
            counter = 1
        selection = 1
    else:
        selection = -1
        counter = 0
    if counter >0:
        counter += 1
        cv2.ellipse(img, (80, 50), (20, 20), 0, 0, counter, (0, 255, 0), 10)


if __name__ == '__main__':
    # remember to open your webcam from laptop
    cap = cv2.VideoCapture(0) # device number = 0
    cap.set(3, WIDTH) # width 
    cap.set(4, HEIGHT) # height
    
    # hand detect
    detector = HandDetector(maxHands=2, detectionCon=0.8)
    
    # communication
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # serverAddressPort = ("127.0.0.1", 5052)
    
    while True:
        get_frame(cap)
    
    cv2.destroyAllWindows()
