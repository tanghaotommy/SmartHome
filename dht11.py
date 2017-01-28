import RPi.GPIO as GPIO
import time

data = []
j=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

time.sleep(1)

GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(16, GPIO.LOW)
time.sleep(0.02)
GPIO.output(16,GPIO.HIGH)
GPIO.setup(16, GPIO.IN)

while GPIO.input(16) == GPIO.LOW:
    continue
while GPIO.input(16) == GPIO.HIGH:
    continue

while j < 40:
    k = 0
    while GPIO.input(16) == GPIO.LOW:
        continue
    while GPIO.input(16) == GPIO.HIGH:
        k += 1
        if k > 100:
            break
    if k < 8 :
        data.append(0)
    else:
        data.append(1)

    j += 1


print "sensor is working"
print data

humidity_bit = data[0:8]
humidity_point_bit = data[8:16]
temperature_bit = data[16:24]
temperature_point_bit = data[24:32]
check_bit = data[32:40]

humidity = 0
humidity_point = 0
temperature = 0
temperature_point = 0
check = 0 

for i in range(8):
    humidity += humidity_bit[i]*2**(7-i)
    humidity_point += humidity_point_bit[i]*2**(7-i)
    temperature += temperature_bit[i]*2**(7-i)
    temperature_point += temperature_point_bit[i] *2 **(7-i)
    check += check_bit[i] *2**(7-i)

tmp = humidity + humidity_point + temperature + temperature_point

if check == tmp:
    print "temperature: ",temperature, "*C, humidity: ",humidity,"%"
else:
    print "wrong"
    print "temperaure: ", temperature, "*C, humidity: ",humidity, "% check: ", check, ", tmp: ",tmp


GPIO.cleanup()
