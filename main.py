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
ultrasonic_1_echo = Pin(10, Pin.IN)
ultrasonic_1_trigger = Pin(11, Pin.OUT)
ultrasonic_2_echo = Pin(12, Pin.IN)
ultrasonic_2_trigger = Pin(13, Pin.OUT)
ultrasonic_3_echo = Pin(14, Pin.IN)
ultrasonic_3_trigger = Pin(15, Pin.OUT)

# main function
def main():
        pass

# Function to calculate the distance using HC-SR04
def measure_distance(trigger_pin, echo_pin):
    # Set up trigger pin as output
    trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
    # Set up echo pin as input
    echo = machine.Pin(echo_pin, machine.Pin.IN)
    
    # Set trigger pin to low for 2 microseconds
    trigger.low()
    time.sleep_us(2)
    
    # Send a 10-microsecond pulse to the trigger pin
    trigger.high()
    time.sleep_us(10)
    trigger.low()
    
    # Measure the duration of the echo pulse
    while echo.value() == 0:
        pass
    start_time = time.ticks_us()
    
    while echo.value() == 1:
        pass
    end_time = time.ticks_us()
    
    # Calculate the distance in centimeters
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    
    return distance


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


if __name__ == '__main__':
    main()
    
    