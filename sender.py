#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time, logging, sys, requests, json, ssl, certifi

#API URL
api='http://192.168.1.101:5000/api/v1.0/setState'

#Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

GPIO.setmode(GPIO.BCM)

#Initialise GPIO Inputs
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Terminal 1
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Terminal 2
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Terminal 3
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Terminal 8

def main():
        try:
                GPIO.add_event_detect(4, GPIO.FALLING, callback=pin4Event, bouncetime=200)
                GPIO.add_event_detect(18, GPIO.FALLING, callback=pin18Event, bouncetime=200)
                GPIO.add_event_detect(17, GPIO.FALLING, callback=pin17Event, bouncetime=200)
                GPIO.add_event_detect(27, GPIO.BOTH, callback=pin27Event, bouncetime=200)

        except KeyboardInterrupt:
                GPIO.cleanup()       # clean up GPIO on CTRL+C exit

        while True:
                time.sleep(10)
def pin4Event(channel):
        pushMessage("reset")
        logging.info("Intruder Alarm Aborted")

def pin18Event(channel):
        pushMessage("confirmed")
        logging.info("Intruder Alarm Confirmed")

def pin17Event(channel):
        pushMessage("triggered")
        logging.info("Intruder Alert Triggered")

def pin27Event(channel):
    if GPIO.input(27):  
        pushMessage("arm")
        logging.info("Alarm Armed")  
    else:                 
        pushMessage("disarm")
        logging.info("Alarm Disarmed") 

def pushMessage(event):
	response = requests.post(api, json = {'state': event})
	logging.info(response.text)
	return True


#Invoke main function
if __name__ == "__main__":
        main()
