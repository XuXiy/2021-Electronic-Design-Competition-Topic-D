import cv2
import time
import numpy as np
 
def videos():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(5,40)
    
    img_num = 0
    k = np.ones((3, 3), np.uint8)  
 
    while True:
        ret, img = cap.read()
 
        if not img_num:
            previous = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_diff = cv2.absdiff(gray, previous)  
        thresh = cv2.threshold(gray_diff, 40, 255, cv2.THRESH_BINARY)[1] 
        mask = cv2.medianBlur(thresh, 3) 
        close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k) 
 
        cnts = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0] 
        for c in cnts:   
            area = cv2.contourArea(c)
            if area > 200:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
        cv2.imshow("thresh_img", close)
        cv2.imshow("Result", img)
        img_num += 1
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
videos()