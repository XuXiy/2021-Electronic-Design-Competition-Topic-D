# -*- coding:utf-8 -*-
import serial
import time
ser = serial.Serial("/dev/ttyAMA0", 115200)
ser.flushInput()  
ser.write("begin".encode("utf-8")) 
def main():
    while True:
        count = ser.inWaiting() 
        if count != 0:
            recv = ser.read(count) 
            ser.write("Recv some data is : ".encode("utf-8"))  
            ser.write(recv)  
            ser.write("\n".encode("utf-8"))  
            print(ser.readline())
            ser.flushInput()

if __name__ == '__main__':
    main()