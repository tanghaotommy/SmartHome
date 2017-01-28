import face3
import requests
import json
import base64

from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()
camera.close()
sleep(10)
face3.StartFaceDetection()




