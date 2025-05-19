import cv2,time,PIL,sys
import socket
import threading
#from queue import Queue
import numpy as np
data = np.zeros((8,128),dtype = np.int8)
def local_threshold(image):
    image = cv2.resize(image, dsize=(128,64))
    gray = cv2.cvtColor(image,cv2.COLOR_BGRA2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 10)
    change = (np.array(binary)).reshape(64,128)
    for y in range(8):
        for x in range(128):
            temp = 0
            for bit in range(8):
                if (change[y*8 + bit][x] == 255):
                    temp |= 0x01 << bit
            data[y][x] = temp  
    print(data)
    #cv2.imshow("binary ", binary)
    socket_con.send(bytes(data))
def job(targenum,change):
    while True:
        socket_con.send(bytes(targenum))
        socket_con.send(bytes(change))
        
def TCP_contect():
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #ip     port
    host_addr = ("192.168.3.75", 8941)
    socket_tcp.bind(host_addr)
    #listen connection request:socket.listen(backlog)
    socket_tcp.listen(1)
    socket_con, (client_ip, client_port) = socket_tcp.accept()
def threshold_demo(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    print("阈值：", ret)
    cv2.imshow("binary", binary)
    
cap = cv2.VideoCapture(0)
if __name__ == '__main__':
    
    kernel_2 = np.ones((2,2),np.uint8)#2x2 convolution
    kernel_3 = np.ones((3,3),np.uint8)#3x3
    kernel_4 = np.ones((4,4),np.uint8)#4x4
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #ip     port
    host_addr = ("192.168.3.75", 8941)
    socket_tcp.bind(host_addr)
    #listen connection request:socket.listen(backlog)
    socket_tcp.listen(1)
    socket_con, (client_ip, client_port) = socket_tcp.accept()
    ##socket_con.send(bytes([1,1,1,0,1,0,1,0,0]))
    #print("Receiving package...")
    while True:
        ret, Img = cap.read()
        #Img = cv2.imread('example.png')#read
        if ret :#is wriitten
            HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)#把BGR图像转换为HSV格式
                
            Lower = np.array([20, 53, 115])#yellow
            Upper = np.array([31, 255, 255])
           # Lower = np.array([20, 86, 208])
           # Upper = np.array([30, 190, 255])                    #mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
            mask = cv2.inRange(HSV, Lower, Upper)
            erosion = cv2.erode(mask,kernel_4,iterations = 1)
            erosion = cv2.erode(erosion,kernel_4,iterations = 1)
            dilation = cv2.dilate(erosion,kernel_4,iterations = 1)
            dilation = cv2.dilate(dilation,kernel_4,iterations = 1)
                    #target是把原图中的非目标颜色区域去掉剩下的图像
            #target = cv2.bitwise_and(Img, Img, mask=dilation)
                    #将滤波后的图像变成二值图像放在binary中
            ret, binary = cv2.threshold(dilation,127,255,cv2.THRESH_BINARY) 
                    #在binary中发现轮廓，轮廓按照面积从小到大排列
            _,contours, hierarchy = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
            p=0
            for i in contours:#遍历所有的轮廓
                area = cv2.contourArea(i)
                if(area>300):
                    x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
                            #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
                    cv2.rectangle(Img,(x,y),(x+w,y+h),(0,255,),3)
                            #给识别对象写上标号
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(Img,str(p),(x-10,y+10), font, 1,(0,0,255),2)#加减10是调整字符位置
                    p +=1
            #print ('黄色方块的数量是',p,'个')#终端输出目标数量
            #cv2.imshow('target', target)
            #cv2.imshow('Mask', mask)
            #cv2.imshow("prod", dilation)
            local_threshold(Img)
            
            #Img = Img.convert(1)
            cv2.imshow('Img', Img)
            #cv2.imwrite('yellow.png', Img)#将画上矩形的图形保存到当前目录        
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break  
