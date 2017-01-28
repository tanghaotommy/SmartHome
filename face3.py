### Imports ###################################################################
from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial

import threading
import cv2
import os
import time
import sys
import requests
import json
import base64


resX = 320
resY = 240

cx = resX / 2
cy = resY / 2

xdeg = 150
ydeg = 150


faceCount = 0

isRunning = True

face_cascade = None

### Helper Functions ##########################################################
def get_faces(img):
    global face_cascade

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    return faces, img

def draw_frame(img, faces):

    global xdeg
    global ydeg
    global cx
    global cy
    global isRunning

    global faceCount

    # Draw a rectangle around every face
    for (x, y, w, h) in faces:

        tx = x + w / 2
        ty = y + h / 2

        if   (cx - tx > 15 and xdeg <= 190):
            xdeg += 1
            os.system("echo 0=" + str(xdeg) + " > /dev/servoblaster")
        elif (cx - tx < -15 and xdeg >= 110):
            xdeg -= 1
            os.system("echo 0=" + str(xdeg) + " > /dev/servoblaster")

        if   (cy - ty > 15 and ydeg >= 110):
            ydeg -= 1
            os.system("echo 1=" + str(ydeg) + " > /dev/servoblaster")
        elif (cy - ty < -15 and ydeg <= 190):
            ydeg += 1
            os.system("echo 1=" + str(ydeg) + " > /dev/servoblaster")

        faceCount += 1
        result = img[y:y + h, x:x + w]
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        result = cv2.resize(result,(100,100),interpolation=cv2.INTER_LINEAR)
        t = time.time()
        cv2.imwrite("face" + str(t) + ".jpg",result)
        print "Save 1 face"

        url = 'http://54.183.198.179/facerecognition.php'
        image =  open("face" + str(t) + ".jpg",'rb')
        image_read = image.read()
        image_64 = base64.encodestring(image_read)
        payload = {"Homename":"home1","Image":image_64}
        r=requests.post(url, data=json.dumps(payload))
        print r.text

        os.remove("face" + str(t) + ".jpg")

        isRunning = False

def main():
    global isRunning
    global face_cascade
    global resX
    global resY


    ### Setup #####################################################################
    os.putenv('SDL_FBDEV', '/dev/fb0')

    os.system("echo 0=150 > /dev/servoblaster")
    os.system("echo 1=150 > /dev/servoblaster")

    # Setup the camera
    camera = PiCamera()
    camera.resolution = (resX, resY)
    camera.framerate = 60

    # Use this as our output
    rawCapture = PiRGBArray(camera, size=(resX, resY))

    camera.start_preview()
    framecount = 0

    isRunning = True

    # The face cascade file to be used
    face_cascade = cv2.CascadeClassifier('/home/pi/seniordesign/haarcascade_frontalface_alt.xml')

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if not isRunning:
            break

        image = frame.array

        face,img = get_faces(image)

        draw_frame(img, face)

        framecount+=1
        if framecount > 20:
            break

        rawCapture.truncate(0)

    rawCapture.truncate(0)
    camera.stop_preview()
    camera.close()

def StartFaceDetection():
    t = threading.Thread(target=main)
    t.start()
