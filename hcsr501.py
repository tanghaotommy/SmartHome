import RPi.GPIO as GPIO
import time
import face3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN)
flag=0

try:
    while True:
        if GPIO.input(12)==0:
            print "nobody"
            flag=0
            time.sleep(0.5)
        if GPIO.input(12)==1:
            print "somebody here"
            if flag==0:
                print "camera on"
                face3.StartFaceDetection()
            flag = 1 
            time.sleep(6)

except KeyboardInterrupt:
    GPIO.cleanup()
    print "all cleanup"

