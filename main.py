# This is code for controlling our robot

import machine
from time import time, sleep
from machine import Pin, PWM, ADC

# pin for motor control
pwm = PWM(Pin(0))
pwm.freq(12000)
max_duty = 65025

adc = ADC(Pin(26))     # create an ADC object
max_adc = 65535
min_adc = 320

# linear interpolation to map a range of values to another (from stackoverflow)
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# funcion for controling one of the motors
# TODO: modify function to be able to controle multiple motors with one funciton
def move_motor(power):

        duty = (translate(power, -1, 1, 0.06, 0.09))
        duty = int(duty * max_duty)
        #print(duty)
        pwm.duty_u16(duty)