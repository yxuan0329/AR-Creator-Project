# -*- coding: utf-8 -*-
import numpy as np
import cv2
import keyboard
import math
from cvzone.HandTrackingModule import HandDetector

# color table 
orange = (0, 69, 255)
light_green = (144, 238, 144)
purple = (128, 0, 128)
pink = (203, 192, 255)

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
    def draw(self, background, coords, color):
        if coords == []:
            return
        points = np.array( [[200, 250]] )
        for coord in coords:
            points = np.append(points, [[int(coord[0]), int(coord[1])]], 0 )        
        cv2.fillConvexPoly(background, points, color)
        

# parameter
WIDTH, HEIGHT = 640, 360 # 1280, 720
selection = -1
select_mode = -1
counter = 0
object_display = False


btn0 = Btn(120, 50)
btn1 = Btn(200, 50)
btn2 = Btn(280, 50)
btn3 = Btn(360, 50)
btn_list = [btn0, btn1, btn2, btn3]
clay = Clay(200, 250, [], pink)

def drawUI(img):
    for btn in btn_list:
        btn.draw(img)
    

def get_frame(cap):
    success, img = cap.read() # get the frame from webcam
    img = cv2.flip(img, 1)

    fingers = [0,0,0,0,0]

    hands, img = detector.findHands(img)
    
    drawUI(img)
    
    global object_display
    data = []
    lmList = []
    # gray_img = spotlight(img, data, fingers)
    
    # landmark values - (x, y, z) * 21
    for hand in hands:        
        lmList = hand['lmList']
        for lm in lmList:
            data.extend([lm[0], lm[1], lm[2]]) # reverse y-dir
                
        fingers = detector.fingersUp(hand) # [1, 1, 1, 1, 1] if fingers up
        print(fingers)
        # print(len(data))
        select_mode = detect_click_btn(img, data, fingers)
        if select_mode == 0:
            clay.coords = generate_points(clay)
            object_display = True
        elif select_mode == 1:
            candle(img, data, fingers)
            new_img = spotlight(img, data, fingers)
            img = new_img
        
    if object_display == True:
        clay.draw(img, clay.coords, clay.color)
    
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
    return select_mode


def generate_points(clay):
    coords = []
    for i in range(0,60):
        theta = math.radians(6 * i)
        x = clay.x + math.sin(theta) * clay.radius
        y = clay.y + math.cos(theta) * clay.radius
        coords.append([x, y])
    return coords

def candle(img, data, fingers):
    if fingers == [1, 0, 0, 0, 0]:
        thumb = FingerTip(int(data[12]), int(data[13]))
        cv2.circle(img, (thumb.x, thumb.y), 10, orange, -1)
   
def in_circle(a, b, radius):
    """ return true if the pixel is inside the circle boundary """
    res = (a.x - b.x) ** 2 + (a.y - b.y) ** 2 - radius ** 2
    return True  if (res <=0) else False
    

def spotlight(img, data, fingers):
    h, w, _ = img.shape
    radius = 50
    
    if fingers == [1, 0, 0, 0, 0]:
        red_img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
        thumb = FingerTip(int(data[12]), int(data[13]))
        for j in range(0, h):
            for i in range(0, w):
                pixel = FingerTip(i, j)
                if in_circle(pixel, thumb, radius):
                    intensity = 1 - distance(pixel, thumb) * 0.02
                    # img[j][i] = (img[j][i][2] * 0.299 + img[j][i][1] * 0.587 + img[j][i][0] * 0.114)  # grayscale RGB = 299, 587, 114   
                    img[j][i] = red_img[j][i]
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(0) # device number = 0
    cap.set(3, WIDTH) # width 
    cap.set(4, HEIGHT) # height
    
    detector = HandDetector(maxHands=2, detectionCon=0.8) # hand detect
    selection = -1

    while True:
        if keyboard.is_pressed("q"):
            print("q is pressed")
            # Key was pressed
            break
        get_frame(cap)
    cap.release()
    cv2.destroyAllWindows()