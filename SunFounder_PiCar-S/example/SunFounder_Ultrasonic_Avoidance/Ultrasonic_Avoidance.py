#!/usr/bin/env python
'''
**********************************************************************
* Filename    : Ultrasonic_Avoidance.py inspired by Ultrasonic_Avoidance_original.py
* Description : Classes for the Ultrasonic sensor and function to read distance
* Author      : Patrick Furtwängler
**********************************************************************
'''
import time
import RPi.GPIO as GPIO

#class for HCSR04 Sensors which I bought
class Ultrasonic_HCSR04(object):

    def __init__(self, Triggerpin, Echopin):
        self.Triggerpin = Triggerpin
        self.Echopin = Echopin
        GPIO.setmode(GPIO.BCM)
    
    def get_distance(self):
        
        #setup
        
        GPIO.setwarnings(False)
        GPIO.setup(self.Triggerpin,GPIO.OUT)
        GPIO.setup(self.Echopin,GPIO.IN)
        
        #send trigger
        
        GPIO.output(self.Triggerpin,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.Triggerpin,GPIO.LOW)
        
        #catch starttime
        while GPIO.input(self.Echopin)==GPIO.LOW:
            buffer = time.time()
        
        time_start=time.time()
        
        #catch endtime
        while GPIO.input(self.Echopin)==GPIO.HIGH:
            buffer = time.time()
            
        time_end=time.time()
        
        duration=time_end-time_start
        
        #calculate distance
        distance = duration*17150
        distance = round(distance,2)
        
        if(distance < 400):
            return distance
        
        #return - as false value indicator
        else:
            return -1


class Ultrasonic_Avoidance(object):
    timeout = 0.05

    def __init__(self, channel):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)

    def distance(self):
        
        pulse_end = 0
        pulse_start = 0
        GPIO.setup(self.channel,GPIO.OUT)
        GPIO.output(self.channel, False)
        time.sleep(0.01)
        GPIO.output(self.channel, True)
        time.sleep(0.00001)
        GPIO.output(self.channel, False)
        GPIO.setup(self.channel,GPIO.IN)

        timeout_start = time.time()
        while GPIO.input(self.channel)==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while GPIO.input(self.channel)==1:
            pulse_end = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1

        if pulse_start != 0 and pulse_end != 0:
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 100 * 343.0 /2
            distance = int(distance)
            #print('start = %s'%pulse_start,)
            #print('end = %s'%pulse_end)
            if distance >= 0:
                return distance
            else:
                return -1
        else :
            #print('start = %s'%pulse_start,)
            #print('end = %s'%pulse_end)
            return -1

    def get_distance(self, mount = 5):
        sum = 0
        for i in range(mount):
            a = self.distance()
            #print('    %s' % a)
            sum += a
        return int(sum/mount)
    def less_than(self, alarm_gate):
        dis = self.get_distance()
        status = 0
        if dis >=0 and dis <= alarm_gate:
            status = 1
        elif dis > alarm_gate:
            status = 0
        else:
            status = -1
        #print('distance =',dis)
        #print('status =',status)
        return status

def test():
    UA = Ultrasonic_Avoidance(20)
    threshold = 10
    while True:
        distance = UA.get_distance()
        status = UA.less_than(threshold)
        if distance != -1:
            print('distance', distance, 'cm')
            time.sleep(0.2)
        else:
            print(False)
        if status == 1:
            print("Less than %d" % threshold)
        elif status == 0:
            print("Over %d" % threshold)
        else:
            print("Read distance error.")
            
def test_HCSR04():
    ua_HC = Ultrasonic_HCSR04(16,12)
    while True:
        distance = ua_HC.get_distance()
        time.sleep(1)

if __name__ == '__main__':
    #test()
    test_HCSR04()