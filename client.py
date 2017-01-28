import paho.mqtt.client as mqtt
import json
from picamera import PiCamera
import requests
import json
import base64
import face3
#import door
#import buzzer
#import light
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/home/home1") #subscribe to corresponding channel (same with the id(unique) of Pi)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    message = json.loads(msg.payload)
    if (message['Type'] == "ViewPhoto"):
        #TO-DO: Require camera to take picture.
        camera = PiCamera()
	camera.start_preview()
	camera.capture('/home/pi/Desktop/viewphoto.jpg')
	camera.stop_preview()
	camera.close()
        url = 'http://54.183.198.179/uploadphoto.php'
	image =  open('/home/pi/Desktop/viewphoto.jpg','rb')
	image_read = image.read()
	image_64 = base64.encodestring(image_read)
	payload = {"Homename":"home1","Image":image_64}
	r=requests.post(url, data=json.dumps(payload))         
    if message['Type'] == "OpenDoor":
    	door.OpenDoor()
    	pass;
    if message['Type'] == "SendAlert":
    	buzzer.alarm()
    	pass;
    if message['Type'] == "TurnOnLight":
    	light.TurnOn()
    	pass;
    if message['Type'] == "TurnOffLight":
    	light.TurnOff()
    	pass;
	if message['Type'] == "HomeStatus":
		url = 'http://54.183.198.179/refreshstatus.php'
		pass
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("54.183.198.179", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
