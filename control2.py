import RPi.GPIO as GPIO
import time
import face3
import paho.mqtt.client as mqtt
import json
from picamera import PiCamera
import requests
import json
import base64
#import door
#import buzzer
#import light
from xbee import ZigBee
import serial
import time
import collections
import sys
import getopt
from socket import *
import traceback
from threading import Thread, Lock
import random
import sys
import Adafruit_DHT


########################
#zigbee
########################


# Communication Parameters
#ZIGBEE_SERIAL_PORT = "/dev/cu.usbserial-DN01DCRH"
ZIGBEE_SERIAL_PORT = "/dev/ttyUSB0"
ZIGBEE_SERIAL_BAUD = 115200
UDP_RECEIVE_PORT = 5005

# Radio Parameters
BROADCAST = '\x00\x00\x00\x00\x00\x00\xff\xff'
UNKNOWN = '\xff\xfe' # This is the 'I don't know' 16 bit address

myLongAddr = 12
myShortAddr = '\xff\xfe' # This is the 'I don't know' 16 bit address
ZIGBEE_DEVICE_ADDRESS = "xxxxxxxxxxxxxxxx"

didGetLocalRadioHighAddress = False;
didGetLocalRadioLowAddress = False;
zb = None

writeAttributeResCheck = False;
enrollmentRspCheck = False;
bindResCheck = False;
matchDescResCh = False;
step = 0;
sensorMacAddr = '\x31\x2E\x78\05\x00\x6F\x0D\x00'

def processZigbeeATCommandMessage(parsedData):
    ''' Method to process an AT zigbee message

        parsedData -- Pre-parsed (into a dict) data from message.
    '''
    global ZIGBEE_DEVICE_ADDRESS
    global didGetLocalRadioHighAddress
    global didGetLocalRadioLowAddress

    # command response for the high bytes of the local device long address
    if(parsedData['command'] == 'SH'):
        # convert the parameter to a string value (human readable)
        value = ""
        for e in parsedData['parameter']:
            value += "{0:02x}".format(ord(e))

        # set the correct portion of the address
        ZIGBEE_DEVICE_ADDRESS = value + ZIGBEE_DEVICE_ADDRESS[8:]
        
        #signal that we got this part of the address
        didGetLocalRadioHighAddress = True

    # command response for the low bytes of the local device long address
    elif(parsedData['command'] == 'SL'):
        # convert the parameter to a string value (human readable)
        value = ""
        for e in parsedData['parameter']:
            value += "{0:02x}".format(ord(e))

        # set the correct portion of the address
        ZIGBEE_DEVICE_ADDRESS = ZIGBEE_DEVICE_ADDRESS[0:8] + value


        #signal that we got this part of the address
        didGetLocalRadioLowAddress = True

def zigbeeHexStringToHexString(zigbeeHexString):
    ''' Method to change string of characters with the hex values to a hex string

        hexList -- string of characters with hex values
    '''

    retString = ''
    for e in zigbeeHexString:
        retString += "{0:02x}".format(ord(e))
    return retString

def hexStringToZigbeeHexString(hexString):
    ''' Method to change a hex string to a string of characters with the hex values

        hexList -- string of hex characters
    '''
    return hexListToChar(splitByN(hexString, 2))

def splitByN(seq, n):
    ''' Method to split a string into groups of n characters

        seq -- string
        n -- group by number
    '''
    return [seq[i:i+n] for i in range(0, len(seq), n)]

def changeEndian(hexString):
    ''' Method to change endian of a hex string

        hexList -- string of hex characters
    '''
    split = splitByN(hexString, 2) # get each byte
    split.reverse();               # reverse ordering of the bytes

    # reconstruct 
    retString = ''
    for s in split:
        retString += s
    return retString

def hexListToChar(hexList):
    ''' Method to convert a list/string of characters into their corresponding values

        hexList -- list or string of hex characters
    '''
    retString = ""
    for h in hexList:
        retString += chr(int(h, 16))
    return retString

	
def parseCommandLineArgs(argv):
    global ZIGBEE_SERIAL_PORT
    global ZIGBEE_SERIAL_BAUD
    try:
        opts, args = getopt.getopt(
            argv, "hp:b:u:", ["port=", "baud=", "udpport="])

    except getopt.GetoptError:
        print 'test.py -p <serial_port> -b <baud_rate> -u <udp_port>'

        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()

        elif opt in ("-p", "--port"):
            ZIGBEE_SERIAL_PORT = arg

        elif opt in ("-b", "--baud"):
            try:
                ZIGBEE_SERIAL_BAUD = int(arg)
            except ValueError:
                print "Buad rate must be an integer"
                sys.exit()

        # elif opt in ("-u", "--udpport"):
        #     try:
        #         UDP_PORT = int(arg)
        #     except ValueError:
        #         print "Udp port must be an integer"
        #         sys.exit()


def printMessageData(data):
    for d in data:
        print d, ' : ',
        for e in data[d]:
            print "{0:02x}".format(ord(e)),
        if (d == 'id'):
            print "({})".format(data[d]),
        print

#this is made by changwoo
def checkRfdata(data):
    count =0
    re = ""
    for d in data:
	if(d=='rf_data'):
	    for e in data[d]:
		if(count>=2):
		    re+="{0:02x}".format(ord(e))
		count=count+1
    return re

def convertMessageToString(data):
    retString = ""

    for d in data:
        retString += d + ' : '

        for e in data[d]:
            retString += "{0:02x}".format(ord(e))

        if (d == 'id'):
            retString += "({})".format(data[d])

        retString += "\n"

    return retString


def splitByN(seq, n):
    ''' Method to split a string into groups of n characters

        seq -- string
        n -- group by number
    '''
    return [seq[i:i+n] for i in range(0, len(seq), n)]


def hexListToChar(hexList):
    retString = ""
    for h in hexList:
        retString += chr(int(h, 16))
    return retString

def getConnectedRadioLongAddress():
    """ Method to make sure we get the MAC address of our local radio"""
    global zb
    # keep looping until we get both the MSBs and the LSBs
    while ((not didGetLocalRadioHighAddress) or (not didGetLocalRadioLowAddress)):

        # reissue requests
        zb.send('at', command="SH")
        zb.send('at', command="SL")
        
        # sleep for a bit to give the radio time to respond before we check again
        time.sleep(0.5)

#this reverseShortAddress method is made by changwoo

def reverseShortAddress(shortAddr):

    #shortAddr = zigbeeHexStringToHexString(myShortAddr)
    result = shortAddr[len(shortAddr)/2:]+shortAddr[0:len(shortAddr)/2]
    #result = hexStringToZigbeeHexString(result)
    return result

def zigbeeMessageCallbackHandler(data):
    global myLongAddr
    global myShortAddr
    global zb
    global writeAttributeResCheck
    global enrollmentRspCheck
    global bindResCheck
    global matchDescResCh
    global step

    try:

        if (data['id'] == 'at_response'):
            processZigbeeATCommandMessage(data)
            print "address=", ZIGBEE_DEVICE_ADDRESS
        elif (data['id'] == 'rx_explicit'):
            myLongAddr = data['source_addr_long']
            myShortAddr = data['source_addr']
            clusterId = (ord(data['cluster'][0]) * 256) + ord(data['cluster'][1])
            profileId = (ord(data['profile'][0]) * 256) + ord(data['profile'][1])

            #	    if (clusterId != 0x06):
            #		if (clusterId !=0x13):
            #		    print 'Cluster ID:', hex(clusterId),
            #		    print "profile id:", repr(data['profile'])
            #		    print "================================================================================"
            #		    printMessageData(data)
            #		    print "================================================================================"

	    #i think useless, ive never seen this is working
	    if (clusterId == 0x0000):
                rfdata = data['rf_data']
                seqNumber = rfdata[0]
                print ''
                print "( 0x0000 ) get NWK Address Request, let's response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
                zb.send('tx_explicit',
                        frame_id='\x08',
                        dest_addr_long=myLongAddr,
                        dest_addr=myShortAddr,
                        src_endpoint='\x00',
                        dest_endpoint='\x00',
                        cluster='\x00\x00',
                        profile='\x00\x00',
                        data=rfdata)
                time.sleep(1)
                zb.send('tx_explicit',
                        frame_id='\x40',
                        dest_addr_long=myLongAddr,
                        dest_addr=myShortAddr,
                        src_endpoint='\x00',
                        dest_endpoint='\x00',
                        cluster='\x80\x00',
                        profile='\x00\x00',
                        data=seqNumber + '\xDA\x9A\xD9\x40\x00\xA2\x13\x00' +'\x00\x00')
                time.sleep(1)


                
            elif ( clusterId == 0x0006 and profileId == 0x0000):
                rfdata = data['rf_data']
                seqNumber = rfdata[0]
                outputClusterList = rfdata[7:]
                print ''
                print "( 0x0006 ) get Match Descriptor Request, let's response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
                zb.send('tx_explicit',
                        frame_id='\x08',
                        dest_addr_long=myLongAddr,
                        dest_addr=myShortAddr,
                        src_endpoint='\x00',
                        dest_endpoint='\x00',
                        cluster='\x00\x06',
                        profile='\x00\x00',
                        data=rfdata)
                time.sleep(1)
                zb.send('tx_explicit',
                            frame_id='\x40',
                            dest_addr_long=myLongAddr,
                            dest_addr=myShortAddr,
                            src_endpoint='\x00',
                            dest_endpoint='\x00',
                            cluster='\x80\x06',
                            profile='\x00\x00',
                            data=seqNumber + '\x00\x00\x00' + '\x01\x01')
                time.sleep(1)

            elif ( clusterId == 0x0006 and profileId == 0x0104):
                rfdata = data['rf_data']
                commandFrame = rfdata[3]
                print ''
                print "( 0x0006 ) get On/Off Report Attributes"
                print 'On/Off : ' + zigbeeHexStringToHexString(commandFrame)
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
                time.sleep(1)

            elif (clusterId == 0x0013):
                rfdata = data['rf_data']
                print ''
                print "( 0x0013 ) get Device Announce, let's response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
                zb.send('tx_explicit',
                        frame_id='\x08',
                        dest_addr_long=myLongAddr,
                        dest_addr=myShortAddr,
                        src_endpoint='\x00',
                        dest_endpoint='\x00',
                        cluster='\x00\x13',
                        profile='\x00\x00',
                        data=rfdata)
                time.sleep(1)


            elif (clusterId ==0x0500):
                rfdata = data['rf_data']
                framecontrol = rfdata[0]
                seqnumber = rfdata[1]
                command = rfdata[2]
                status = rfdata[3]
                print ''
                print "( 0x0500 ) "
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)

		if(seqnumber == '\xe1'):
		    print "get enrollment response"

		if(seqnumber == '\xab'):
		    print "get write attribute response"

                    if (command == '\x04' and status == '\x00'):
                        print 'get write attribute response success'
		        step= step+1


		#useless
                if(command == '\x00'):
                    print 'get Zone status change notification'
                    zb.send('tx_explicit',
                            frame_id='\x40',
                            dest_addr_long=myLongAddr,
                            dest_addr=myShortAddr,
                            src_endpoint='\x01',
                            dest_endpoint='\x01',
                            cluster='\x05\x00',
                            profile='\x01\x04',
                            data='\x00' + seqnumber + '\x0b\x00\x81')
                    time.sleep(1)

            elif (clusterId == 0x8004):
                rfdata = data['rf_data']
                status = rfdata[1]
                print ''
                print "( 0x8004 ) get Simple descriptor Response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
		if status == '\x00':
		    step= step+1



            elif (clusterId == 0x8005):
                rfdata = data['rf_data']
                status = rfdata[1]
                print ''
                print "( 0x8005 ) get Active Endpoint Response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
		if status =='\x00':
		    step= step+1




            elif (clusterId == 0x8006):
                rfdata = data['rf_data']
                print ''
                print "( 0x8006 ) get Match Descriptor Response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)


            elif (clusterId ==0x8021):
                rfdata = data['rf_data']
                statuss = rfdata[1]
                print ''
                print "( 0x8021 ) bind Response"
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
                if statuss=='\x00':
                    step= step+1

            elif (clusterId ==0x0b04):
                rfdata = data['rf_data']
                seqnumber = rfdata[1]
                commandFrame = rfdata[2]
                status = rfdata[3]
                print ''
                if status=='\x00':
                    print "( 0x0b04 ) configure reporting response success "
                    zb.send('tx_explicit',
                            frame_id='\x40',
                            dest_addr_long=myLongAddr,
                            dest_addr=myShortAddr,
                            src_endpoint='\x01',
                            dest_endpoint='\x01',
                            cluster='\x0b\x04',
                            profile='\x01\x04',
                            data='\x00' + seqnumber + '\x0b'+'\x07'+'\x00')
                    time.sleep(1)
             


                elif commandFrame =='\x0a':
                    print "( 0x0b04 ) Electrical Measurement Report Attributes"
                    watts = (ord(rfdata[7]) * 256) + ord(rfdata[6])
                    print "watts : " + str(watts)

                else :
                    print "( 0x0b04 ) ..."
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)

            else:
                rfdata = data['rf_data']
                seqNumber = rfdata[1]
                print ''
                print "( " + hex(clusterId) + " ) ..."
                print 'rfdata : ' + zigbeeHexStringToHexString(rfdata)
		
#	else:
#	    #these 2 print sentences are made by changwoo 
#	    print '------------------this data is not at or rx--------------------'
#	    printMessageData(data)
#	    print '---------------------------------------------------------------'

    except:
	print "I didn't expect this error:", sys.exc_info()[0]
	traceback.print_exc()

######################
#client
######################
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
    id = message['Id'] #add
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
        payload = {"Homename":"home1","Id":id,"Image":image_64} #modified
        r=requests.post(url, data=json.dumps(payload))         
    if message['Type'] == "OpenDoor":
        door.OpenDoor()
        pass;
    if message['Type'] == "SendAlert":
        GPIO.setup(23, GPIO.OUT)
        for i in range(0,10):
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.075)
            GPIO.output(23, GPIO.LOW)
            time.sleep(0.075)
        pass;
    if message['Type'] == "TurnOnLight":
        print 'sending Turn On'
        zb.send('tx_explicit',
            frame_id='\x40',
            dest_addr_long=myLongAddr,
            dest_addr=myShortAddr,
            src_endpoint='\x01',
            dest_endpoint='\x01',
            cluster='\x00\x06',
            profile='\x01\x04',
            data='\x01' + '\x04'+ '\x01')
        pass;
    if message['Type'] == "TurnOffLight":
        print 'sending Turn Off'
        zb.send('tx_explicit',
            fame_id='\x40',
            dest_addr_long=myLongAddr,
            dest_addr=myShortAddr,
            src_endpoint='\x01',
            dest_endpoint='\x01',
            cluster='\x00\x06',
            profile='\x01\x04',
            data='\x01' + '\x04'+ '\x00')
        pass;
    if message['Type'] == "HomeStatus":
        url = 'http://54.183.198.179/refreshstatus.php'
        humidity, temperature = Adafruit_DHT.read_retry(11,4)
        print 'Temperature: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
        pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("54.183.198.179", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN)
flag=0


# parse the command line arguments
parseCommandLineArgs(sys.argv[1:])
# create serial object used for communication to the zigbee radio
serialConnection = serial.Serial(ZIGBEE_SERIAL_PORT, ZIGBEE_SERIAL_BAUD)
   
# create a zigbee object that handles all zigbee communication
# we use this to do all communication to and from the radio
# when data comes from the radio it will get a bit of unpacking
# and then a call to the callback specified will be done with the 
# unpacked data
zb = ZigBee(serialConnection, callback=zigbeeMessageCallbackHandler)

getConnectedRadioLongAddress();
    
time.sleep(1)
print "Broadcasting route record request "
zb.send('tx_explicit',
    dest_addr_long = BROADCAST,
    dest_addr = UNKNOWN,
    src_endpoint = '\x00',
    dest_endpoint = '\x00',
    cluster = '\x00\x32',
    profile = '\x00\x00',
    data = '\x12'+'\x01')
time.sleep(6)

    
print "Sending configure reports"
    
print "Starting main loop..."


global step
global sensorMacAddr



try:
    while True:
        #zigbee connection
        # print "sending"
        # Management Permit Joining Request. just send one time.
        if step == 0:
            print "sending Management Permit Joining Request"
            zb.send('tx_explicit',
                    frame_id='\x08',
                    dest_addr_long=myLongAddr,
                    dest_addr=myShortAddr,
                    src_endpoint='\x00',
                    dest_endpoint='\x00',
                    cluster='\x00\x36',
                    profile='\x00\x00',
                    data='\x01' + '\x5a' + '\x00')
            time.sleep(1)
            step = step+1



        elif step == 1:
            print "sending Management Permit Joining Request"
            zb.send('tx_explicit',
                    frame_id='\x01',
                    dest_addr_long=myLongAddr,
                    dest_addr=myShortAddr,
                    src_endpoint='\x00',
                    dest_endpoint='\x00',
                    cluster='\x00\x36',
                    profile='\x00\x00',
                    data='\x01' + '\x5a' + '\x00')
            time.sleep(1)
            step = step+1

        elif step == 2:
            print "sending Binding Request"
            zb.send('tx_explicit',
                    frame_id='\x40',
                    dest_addr_long=myLongAddr,
                    dest_addr=myShortAddr,
                    src_endpoint='\x00',
                    dest_endpoint='\x00',
                    cluster='\x00\x21',
                    profile='\x00\x00',
                    data='\x02' + '\x78\x7A\x77\x05\x00\x6F\x0D\x00'+'\x01'+'\x04\x0B'+'\x03'+'\xDA\x9A\xD9\x40\x00\xA2\x13\x00'+'\x01')
            time.sleep(1)
            step = step+1

        elif step == 3:
            print "sending Configure Reporting"
            zb.send('tx_explicit',
                    frame_id='\x40',
                    dest_addr_long=myLongAddr,
                    dest_addr=myShortAddr,
                    src_endpoint='\x01',
                    dest_endpoint='\x01',
                    cluster='\x0B\x04',
                    profile='\x01\x04',
                    data='\x00' + '\x03'+ '\x06'+ '\x00'+'\x0b\x05'+'\x29'+'\x01\x00'+'\x58\x02'+'\x05\x00')
            time.sleep(1)
            step=step+1
        
        #################
        #human sensor
        #################
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
        client.loop_stop()
        zb.halt()
        serialConnection.close()
        print "all cleanup"
except:
        traceback.print_exc()

zb.halt()
serialConnection.close()
GPIO.cleanup()
client.loop_stop()





