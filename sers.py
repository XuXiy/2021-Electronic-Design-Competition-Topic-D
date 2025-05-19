import serial
import time 

if ser.Open():
    ser.flushInput()
else:
    ser=serial.Serial("/dev/ttyAMA0",9600)

while True:
    count = ser.inWaiting()
    if count!=0:
        recv = ser.read(count)
        ser.write("recv = ")
        ser.write(recv)
        ser.flushInput()