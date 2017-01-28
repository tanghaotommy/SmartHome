### Imports ###################################################################

from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial

import threading
import cv2
import os
import time
import sys


### Setup #####################################################################

os.putenv( 'SDL_FBDEV', '/dev/fb0' )

resX = 320
resY = 240

cx = resX / 2
cy = resY / 2

os.system( "echo 0=150 > /dev/servoblaster" )
os.system( "echo 1=150 > /dev/servoblaster" )

xdeg = 150
ydeg = 150


# Setup the camera
camera = PiCamera()
camera.resolution = ( resX, resY )
camera.framerate = 60

# Use this as our output
rawCapture = PiRGBArray( camera, size=( resX, resY ) )

# The face cascade file to be used
face_cascade = cv2.CascadeClassifier('/home/pi/seniordesign/haarcascade_frontalface_alt.xml')

faceCount = 0

isRunning = True

### Helper Functions ##########################################################

def get_faces( img ):

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    faces = face_cascade.detectMultiScale( gray )

    return faces, img

def draw_frame( img, faces ):

    global xdeg
    global ydeg
    global isRunning

    global faceCount

    # Draw a rectangle around every face
    for ( x, y, w, h ) in faces:

        #cv2.rectangle( img, ( x, y ),( x + w, y + h ), ( 200, 255, 0 ), 2 )
        #cv2.putText(img, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

        tx = x + w/2
        ty = y + h/2

        if   ( cx - tx > 15 and xdeg <= 190 ):
            xdeg += 1
            os.system( "echo 0=" + str( xdeg ) + " > /dev/servoblaster" )
        elif ( cx - tx < -15 and xdeg >= 110 ):
            xdeg -= 1
            os.system( "echo 0=" + str( xdeg ) + " > /dev/servoblaster" )

        if   ( cy - ty > 15 and ydeg >= 110 ):
            ydeg -= 1
            os.system( "echo 1=" + str( ydeg ) + " > /dev/servoblaster" )
        elif ( cy - ty < -15 and ydeg <= 190 ):
            ydeg += 1
            os.system( "echo 1=" + str( ydeg ) + " > /dev/servoblaster" )


        faceCount += 1
        result = img[y:y+h, x:x+w]
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        result = cv2.resize(result,(100,100),interpolation=cv2.INTER_LINEAR)
        cv2.imwrite("face" + str(faceCount) + ".jpg",result)
        print "Save 1 face"
        isRunning = False

def main():
    global isRunning
    
    for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
        if not isRunning:
            break

        image = frame.array

        face,img = get_faces(image)

        draw_frame(img, face)

        rawCapture.truncate( 0 )

    rawCapture.truncate(0)

def StartFaceDetection():
    t = threading.Thread(target=main)
    t.start()
