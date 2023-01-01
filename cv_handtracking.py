# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 20:23:34 2022

@author: xuan
"""

import cv2
import keyboard
from cvzone.HandTrackingModule import HandDetector
<<<<<<< Updated upstream
# import socket
=======


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
        
        
class Clay:
    def __init__(self, x, y, coords, color):
        self.x = x
        self.y = y
        self.radius = 40
        self.coords = coords
        self.color = color
    def draw(self, background, coords):
        if coords == []:
            return
        first_coord = []
        curr_coord = []
        for coord in coords:
            coord[0] = int(coord[0]) # change float to integer for drawing
            coord[1] = int(coord[1])
            cv2.circle(background, (coord[0], coord[1]), 2, (0, 0, 127), -1)
            if first_coord == []: # store the first coords
                first_coord.append(coord[0])
                first_coord.append(coord[1])
            else:
                cv2.line(background, (curr_coord[0], curr_coord[1]), (coord[0], coord[1]), 2, cv2.LINE_AA)
            curr_coord = [coord[0], coord[1]]
        cv2.line(background, (curr_coord[0], curr_coord[1]), (first_coord[0], first_coord[1]), 2, cv2.LINE_AA)
        
>>>>>>> Stashed changes

# parameter
WIDTH, HEIGHT = 640, 360 # 1280, 720
selection = -1
counter = 0
<<<<<<< Updated upstream
=======


btn0 = Btn(120, 50)
btn1 = Btn(200, 50)
btn2 = Btn(280, 50)
btn3 = Btn(360, 50)
btn_list = [btn0, btn1, btn2, btn3]
c = []
clay = Clay(200, 250, c, (0, 255, 0))

def drawUI(img):
    for btn in btn_list:
        btn.draw(img)
>>>>>>> Stashed changes
    


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
<<<<<<< Updated upstream
    # print(len(data))
    # sock.sendto(str.encode(str(data)), serverAddressPort)
        
    showUI(img)
    click_btn(fingers, img)
=======
        # print(len(data))
        select_mode = detect_click_btn(img, data, fingers)
        if select_mode == 0:
            clay.coords = generate_points(clay)
            clay.draw(img, clay.coords)
>>>>>>> Stashed changes
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

def showUI(img):
    cv2.ellipse(img, (80, 50), (20, 20), 0, 0, 360, (0, 255, 255), -1)
    cv2.ellipse(img, (80, 110), (20, 20), 0, 0, 360, (0, 255, 255), -1)
    cv2.ellipse(img, (80, 170), (20, 20), 0, 0, 360, (0, 255, 255), -1)
    cv2.ellipse(img, (80, 230), (20, 20), 0, 0, 360, (0, 255, 255), -1)

def click_btn(fingers, img):
    global selection, counter
    counterspeed = 5
    if fingers == [0, 1, 0, 0, 0]: # point "1"
        if selection != 1:
            counter = 1
        selection = 1
    else:
        selection = -1
        counter = 0
    if counter > 0 and counter * counterspeed <= 360:
        counter += 1
        print (counter, selection)
<<<<<<< Updated upstream
        cv2.ellipse(img, (80, 50), (20, 20), 0, 0, counter * counterspeed, (0, 255, 0), 10)
=======
        cv2.ellipse(img, (btn_list[selection].x, btn_list[selection].y), (btn_list[selection].radius, btn_list[selection].radius), 0, 0, counter * counterspeed, (0, 255, 0), 10)
        if counter * counterspeed >= 360:
            select_mode = selection
            print ("enter mode " + str(selection))
            counter = 0
            selection = -1
    return select_mode


def generate_points(clay):
    coords = []
    for i in range(0,60):
        theta = math.radians(6 * i)
        x = clay.x + math.sin(theta) * clay.radius
        y = clay.y + math.cos(theta) * clay.radius
        coords.append([x, y])
    return coords
>>>>>>> Stashed changes


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
    selection = -1
    while True:
        get_frame(cap)
    
    cv2.destroyAllWindows()
