import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

beep = 18
led1 = 22
key1 = 12
key2 = 16


GPIO.setup(beep,GPIO.OUT,initial=GPIP.LOW)
GPIO.setup(led1,GPIO.OUT,initial=GPIP.LOW)
GPIO.setup(key1,GPIO.IN)
GPIO.setup(key2,GPIO.IN)

pwm.GPIO.PWM(beep,200)
while True:
    if GPIO.input(key1):
        pwm.stop()
        GPIO.output(led1,GPIO.LOW)
    else:
        pwm.start(1)
        GPIO.output(led1,GPIO.HIGH)