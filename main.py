import RPi.GPIO as GPIO
import time
import picamera
import urllib.request

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

pir_pin = 24 #GPIO
red_led = 23 #GPIO
green_led = 25 #GPIO
camera=picamera.PiCamera()
buzzer = 13 #GPIO
ldr = 22 #GPIO

GPIO.setup(pir_pin, GPIO.IN) #GPIO INPUT
GPIO.setup(red_led, GPIO.OUT) #GPIO OUTPUT
GPIO.setup(green_led, GPIO.OUT) #GPIO ONPUT
GPIO.setup(buzzer, GPIO.OUT) #GPIO OUTPUT
GPIO.setup(ldr, GPIO.IN) #GPIO INPUT

GPIO.output(red_led, False) #Red LED OFF
GPIO.output(green_led, False) #Green LED OFF


myAPI = '1Z9A8ALS5IULVU3D' #APIkey
baseURL = "http://api.thingspeak.com/update?api_key=%s"% myAPI

print("waiting for sensor to settle")
try:
    while True:

        input_state = GPIO.input(pir_pin)
        LDR_state = GPIO.input(22)
        
        if input_state == True:
            GPIO.output(red_led, True) #Red LED ON
            GPIO.output(green_led, False) #Green LED OFF
            print("Motion Detected!")

            detect = 1
            
            url = baseURL+"&field1=%s" % (detect)
            conn = urllib.request.urlopen(url)
            print(conn.read())
            conn.close()   #Closing the connection
            time.sleep(1)

            for i in range(5):#Capture 5 image
                    camera.capture("newimage%s.jpg"%i, use_video_port=True)
                    time.sleep(2)

            if LDR_state == False:
                GPIO.output(13, False) #Buzzer OFF
                print("Normal")
                time.sleep(0.5)

            else:
                GPIO.output(13, True) #Buzzer ON
                print("Intruder!")
                time.sleep(0.5)
                    
                       
        else:
            GPIO.output(green_led, True) #Green LED ON
            GPIO.output(red_led, False) #Red LED
            print("Motion Not Detected")
                  
            detect = 0
            
            url = baseURL+"&field1=%s" % (detect)
            conn = urllib.request.urlopen(url)
            print(conn.read())
            conn.close()   #Closing the connection
            time.sleep(1)


except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
