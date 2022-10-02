#!/usr/bin/env python
'''
**********************************************************************
* Filename    : Mainprogramm.py
* Description : Main Programm for my Picar
* Author      : Patrick Furtwängler
**********************************************************************
'''

from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import time
import picar
import random
from pyPS4Controller.controller import Controller
import RPI.GPIO as GPIO
import Soundmodule as sound

picar.setup()

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
rightsensor = Ultrasonic_Avoidance.Ultrasonic_HCSR04(26,19)
leftsensor = Ultrasonic_Avoidance.Ultrasonic_HCSR04(16,12)

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

#setup

fw.turning_max = 45
forward_speed = 70
backward_speed = 50

turn_distance = 10

timeout = 10
last_angle = 90
last_dir = 0

def turn_90_deg_over_rightside():
    bw.speed = 70
    bw.backward()
    fw.turn_left()
    time.sleep(1.3)
    fw.turn_right()
    bw.forward()
    time.sleep(1.3)
    stop()
    
def turn_90_deg_over_leftside():
    bw.speed = 70
    bw.backward()
    fw.turn_right()
    time.sleep(1.3)
    fw.turn_left()
    bw.forward()
    time.sleep(1.3)
    stop()

def start_avoidance():
    print('start_avoidance')
    
    bw.forward()
    bw.speed = forward_speed
    fw.turn_straight()
    
    #initialize distances from the sensors
    distance = ua.get_distance()
    rightsensor_distance = rightsensor.get_distance()
    leftsensor_distance = leftsensor.get_distance()

    while True:
        #initialize distances from the sensors
        distance = ua.get_distance()
        rightsensor_distance = rightsensor.get_distance()
        leftsensor_distance = leftsensor.get_distance()
        
        #avoid bad values from new HCSR04 Sensor
        while(rightsensor_distance == -1):
            rightsensor_distance = rightsensor.get_distance()
            
        while(leftsensor_distance == -1):
            leftsensor_distance = leftsensor.get_distance()
            
        print("distance: %scm" % distance)
        print("rightsensor_distance: %scm" % rightsensor_distance)
        print("leftsensor_distance: %scm" % leftsensor_distance)
        
        if distance < 50:
            
            #leichtes ausweichen anhand der Sensordaten links rechts      
            print("distance is < 50cm")
            if leftsensor_distance > rightsensor_distance:
                if leftsensor_distance > distance:
                    fw.turn(70) # 90deg is straight 70 is 20deg left
                    bw.forward()
                else:
                    bw.forward()
                    fw.turn_straight()
            
            if rightsensor_distance > leftsensor_distance:
                if rightsensor_distance > distance: 
                    fw.turn(110) # 20deg right
                    bw.forward()
                else:
                    fw.turn_straight()
                    bw.forward()
            #turn
            if(distance < turn_distance):
                if leftsensor_distance > rightsensor_distance:
                    turn_90_deg_over_leftside()
                    turn_90_deg_over_leftside()
                    bw.forward()
                    bw.speed = forward_speed
                else:
                    turn_90_deg_over_rightside()
                    turn_90_deg_over_rightside()
                    bw.forward()
                    bw.speed = forward_speed

        else:                       # forward
            fw.turn_straight()
            bw.forward()
            bw.speed = forward_speed

def stop():
    bw.stop()
    fw.turn_straight()

# Translate analog controller input values into motor output values
def transfer_Analog_throttle(value):
    x = (value+32767)/65534
    # Filter values that are too low
    if abs(x) < 0.25:
        return 0
    # Return a value between 0.3 and 1.0
    else:
        return round(x, 2)
    
def transfer_Analog_steering(value):
    x = value/32767 #32767 is max value of the analog Sticks
    round(x, 2)
    return x*45 #return 45degree angle
    
class MyController(Controller):
    #redefining all Functions that are called upon the Controller Input
    def __init__(self, **kwargs):
       Controller.__init__(self, **kwargs)
       
    #triangle to start avoidance
    def on_triangle_press(self):
        start_avoidance()
    #sounds
    def on_circle_press(self):
        sound.Horn()
        
    def on_square_press(self):
        sound.Reverse()
        
    def on_x_press(self):
        sound.Throttle()
        
    #moveing the picar with arrow keys
    def on_up_arrow_press(self):
        print("up Arrow pressed, moving forwards")
        bw.forward()
        bw.speed = 100
    
    def on_down_arrow_press(self):
        print("down Arrow pressed, moving backwards")
        bw.backward()
        bw.speed = 100

    def on_up_down_arrow_release(self):
        print("up/down Arrow released, stopping backwheels")
        bw.speed = 0
        
    def on_left_arrow_press(self):
        print("left Arrow pressed, turning left")
        fw.turn_left()
    
    def on_right_arrow_press(self):
        print("left Arrow pressed, turning right")
        fw.turn_right()
        
    def on_left_right_arrow_release(self):
        print("left/right Arrow released, Wheels straigt")
        fw.turn_straight()
        
#moveing the Picar with Analog Input keys from the Controller
        
        #forward
    def on_R2_press(self, value): 
        value = transfer_Analog_throttle(value)
        bw.forward()
        bw.speed = int(value*100)
        print("R2 pressed, moving forward Speed = ",value*100)
        
        #backward
    def on_L2_press(self, value):
        value = transfer_Analog_throttle(value)
        bw.backward()
        bw.speed = int(value*100)
        print("L2 pressed, moving backwards Speed =",value*100)
        
        #stop on release
    def on_R2_release(self):
        print("R2 released, stopping")
        bw.speed = 0
        
        #stop on release
    def on_L2_release(self):
        print("L2 released, stopping")
        bw.speed = 0
        
        #turn left on Analog input
    def on_L3_left(self, value):
        value = value *-1 # *-1 because turning stick left gives negative values
        value = transfer_Analog_steering(value)
        fw.turn(int(90-value))
        print("L3 left, turning",value,"degrees","left")
        
        #turn right on Analog input
    def on_L3_right(self, value):
        value = transfer_Analog_steering(value)
        fw.turn(int(90+value))
        print("L3 right, turning",value,"degrees","right")
        
    def on_L3_x_at_rest(self):
        print("L3 at rest, turning Wheels straight")
        fw.turn_straight()
        

if __name__ == '__main__':
    
    #setting up Controller with interface js0 (default name for only connected joystick)
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    #listen to controller Inputs, time to connect the controller is set to 60s
    controller.listen(timeout = 60)
    