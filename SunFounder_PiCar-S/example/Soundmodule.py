'''
**********************************************************************
* Filename    : Soundmodule.py
* Description : Soundmodule for my Picar
* Author      : Patrick Furtwängler
**********************************************************************
'''


import RPi.GPIO as GPIO
import time

#setting up GPIO pins
Hornpin = 5
Throttlepin = 6
Reversepin = 13

GPIO.setmode(GPIO.BCM)

#set Soundpins as Output
GPIO.setup(Hornpin,GPIO.OUT)
GPIO.setup(Throttlepin,GPIO.OUT)
GPIO.setup(Reversepin,GPIO.OUT)

#Trigger the sound by setting Pins Low with these Functions
def Horn():
    
    #set other pins as input to avoid disturbance
    GPIO.setup(Throttlepin,GPIO.IN)
    GPIO.setup(Reversepin,GPIO.IN)
    
    GPIO.output(Hornpin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(Hornpin,GPIO.HIGH)
    
    #setting other pins back to outputs
    GPIO.setup(Throttlepin,GPIO.OUT)
    GPIO.setup(Reversepin,GPIO.OUT)

def Throttle():
    
    GPIO.setup(Hornpin,GPIO.IN)
    GPIO.setup(Reversepin,GPIO.IN)
    
    GPIO.output(Throttlepin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(Throttlepin,GPIO.HIGH)
    
    GPIO.setup(Hornpin,GPIO.OUT)
    GPIO.setup(Reversepin,GPIO.OUT)
    
def Reverse():
    
    GPIO.setup(Hornpin,GPIO.IN)
    GPIO.setup(Throttlepin,GPIO.IN)
    
    GPIO.output(Reversepin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(Reversepin,GPIO.HIGH)
    
    GPIO.setup(Hornpin,GPIO.OUT)
    GPIO.setup(Throttlepin,GPIO.OUT)
    
    
    