import io
import socket
import struct
import cv2
import numpy as np
from PIL import Image
import math
import time
import serial

time.sleep(6)
g=9.80665
a=24.8406
T=0
lowloca=0
num=0
L=0
x_array = np.zeros(80)
index = -1
startcommend=1
measurecom=0
timestart=0
dirc = -1
sercommand = np.array(1,4)
zero_num = -2

if ser.Open():
    ser.flushInput()
else:
    ser=serial.Serial("/dev/ttyAMA0",9600)

if __name__ == '__main__':
    
    kernel_2 = np.ones((2,2),np.uint8)#2x2 convolution
    kernel_3 = np.ones((3,3),np.uint8)#3x3
    kernel_4 = np.ones((4,4),np.uint8)#4x4
    server_socket = socket.socket()
    server_socket.bind(('192.168.0.10', 8091))
    server_socket.listen(0)
    
    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')    
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with opencv and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            
            data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
            imagedisp = cv2.imdecode(data, 1)
            cv2.imwrite("img.jpg",imagedisp)
            HSV = cv2.cvtColor(imagedisp, cv2.COLOR_BGR2HSV)#把BGR图像转换为HSV格式
            
            mask = cv2.inRange(HSV, Lower, Upper)
            erosion = cv2.erode(mask,kernel_4,iterations = 1)
            erosion = cv2.erode(erosion,kernel_4,iterations = 1)
            dilation = cv2.dilate(erosion,kernel_4,iterations = 1)
            dilation = cv2.dilate(dilation,kernel_4,iterations = 1)
            ret, binary = cv2.threshold(dilation,127,255,cv2.THRESH_BINARY) 
                    #在binary中发现轮廓，轮廓按照面积从小到大排列
            contours, hierarchy = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
             
            if contours:
                maxrect = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(maxrect)#将轮廓分解为识别对象的左上角坐标和宽、高
                                    #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
                cv2.rectangle(imagedisp,(x-7,y-7),(x+w+5,y+h+5),(0,0,255),2)
                x = x+(w/2)
                if startcommend:
                    index+=1
                    x_array[index]=x
                    if index>=79:
                        index=-1
                        lowloca = (np.max(x_array)+np.min(x_array))/2
                        
                        sercommand[0][0] = (lowloca - np.min(x_array))/255
                        sercommand[0][1] = (lowloca - np.min(x_array))%255 
                        measurecom = 1
                        x_array=np.zeros(80)
            sercommand[0][4]=0
            print(time.time() - start_time)
            if measurecom:
                startcommend=0
                if x>=lowloca:
                    if dirc<0:
                        zero_num += 1
                        if(zero_num==0)
                            timestart = time.time()
                    dirc = 1
                if x<lowloca:
                    if dirc>0:
                        zero_num += 1
                        if(zero_num==0)
                            timestart = time.time()
                        else:
                            T = time.time() - start_time
                            if T>=20.0:
                                L = 4*T*T*a-7.5
                                sercommand[0][3]=L
                                sercommand[0][4]=1
                    dirc = -1 
                    #给识别对象写上标号

            ser.write(sercommand)
            font=cv2.FONT_HERSHEY_SIMPLEX
                    #cv2.putText(Img,str(p),(x-10,y+10), font, 1,(0,0,255),2)#加减10是调整字符位置
            #cv2.imshow('Img', imagedisp)       
            #cv2.imshow('mask', mask)
            #cv2.imshow('dilation', dilation)
            #cv2.imshow('erosion', erosion)
            cv2.imshow("Img",imagedisp)
            cv2.imshow("Frame",imagedisp)
            cv2.moveWindow("Img",100,100)
            cv2.moveWindow("Frame",1000,100)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break   
    finally:
        connection.close()
        server_socket.close()

