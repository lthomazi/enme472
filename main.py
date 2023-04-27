''' 
This is code for controlling our robot. The code will have to:
    - control two motors
    - control soleid valves for water control
    - measure distance of two ultrasonic sensors
'''
import machine
from time import utime, sleep
from machine import Pin, PWM, ADC
import _thread as thread

# Solenoid control
solenoid = Pin(22, Pin.OUT)

# Ultrasonic sensor
ultrasonic_1_echo = Pin(11, Pin.IN)
ultrasonic_1_trigger = Pin(12, Pin.OUT)
ultrasonic_2_echo = Pin(11, Pin.IN)
ultrasonic_2_trigger = Pin(12, Pin.OUT)


# pin for motor control
pwm = PWM(Pin(0))
pwm.freq(12000)
max_duty = 65025

adc = ADC(Pin(26))     # create an ADC object
max_adc = 65535
min_adc = 320

# read distance from ultrasonic
def read_distance(sensor_number):
    if sensor_number == 1:
        ultrasonic_1_trigger.low()
        utime.sleep(2)
        ultrasonic_1_trigger.high()
        utime.sleep(5)
        ultrasonic_1_trigger.low()
       
        while ultrasonic_1_echo.value() == 0:
            signaloff1 = utime.ticks_us()
        
        while echo.value() == 1:
            signalon1 = utime.ticks_us()
        
        timepassed1 = signalon1 - signaloff1
        distance1 = (timepassed1 * 0.0343) / 2
        print("Sensor 1: ", distance1, " cm")

    elif sensor_number == 2:
        ultrasonic_2_trigger.low()
        utime.sleep(2)
        ultrasonic_2_trigger.high()
        utime.sleep(5)
        ultrasonic_2_trigger.low()
       
        while ultrasonic_2_echo.value() == 0:
            signaloff2 = utime.ticks_us()
        
        while echo.value() == 1:
            signalon2 = utime.ticks_us()
        
        timepassed2 = signalon2 - signaloff2
        distance2 = (timepassed2 * 0.0343) / 2
        print("Sensor 2: ", distance2, " cm")
    
    else:
        raise Exception("no utrasonic sensor selected")


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