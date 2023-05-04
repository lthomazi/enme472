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

# Solenoid control pins
solenoid = Pin(22, Pin.OUT)

# Ultrasonic sensor pins
ultrasonic_1_echo = Pin(10, Pin.IN)
ultrasonic_1_trigger = Pin(11, Pin.OUT)
ultrasonic_2_echo = Pin(12, Pin.IN)
ultrasonic_2_trigger = Pin(13, Pin.OUT)
ultrasonic_3_echo = Pin(14, Pin.IN)
ultrasonic_3_trigger = Pin(15, Pin.OUT)

# motor control pins
motor1 = Pin(18, Pin.OUT)
motor2 = Pin(19, Pin.OUT)
motor3 = Pin(20, Pin.OUT)
motor4 = Pin(21, Pin.OUT)

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


def forward():
    pass

if __name__ == '__main__':
    main()
    
    