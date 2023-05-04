''' 
This is code for controlling our robot. The code will have to:
    - control two motors
    - control soleid valves for water control
    - measure distance of two ultrasonic sensors
'''

import machine
from time import time, sleep
from machine import Pin, PWM, ADC
import _thread as thread

# Solenoid control pins
solenoid = Pin(22, Pin.OUT)

# Ultrasonic sensor pins
ultrasonic_1_echo = Pin(10, Pin.IN)
ultrasonic_1_trigger = Pin(11, Pin.OUT)
ultrasonic_2_echo = Pin(12, Pin.IN)
ultrasonic_2_trigger = Pin(13, Pin.OUT)

# motor control pins
motor1 = Pin(18, Pin.OUT)
motor2 = Pin(19, Pin.OUT)
motor3 = Pin(20, Pin.OUT)
motor4 = Pin(21, Pin.OUT)

# solenoid-relay pins
solenoid = Pin(22,Pin.OUT)
solenoid.value(0)

# Open or close solenoid
def turn_on_solenoid():
    solenoid.on()
    time.sleep(0.5)

def turn_off_solenoid():
    solenoid.off()
    time.sleep(0.5)

    


# main function
def main():
        pass

# Function to calculate the distance using HC-SR04
def measure_distance_1():

    ultrasonic_1_echo = Pin(10, Pin.IN)
    ultrasonic_1_trigger = Pin(11, Pin.OUT)
    
    # Set trigger pin to low for 2 microseconds
    ultrasonic_1_trigger.low()
    time.sleep_us(2)
    
    # Send a 10-microsecond pulse to the trigger pin
    ultrasonic_1_trigger.high()
    time.sleep_us(10)
    ultrasonic_1_trigger.low()
    
    # Measure the duration of the echo pulse
    while ultrasonic_1_echo.value() == 0:
        pass
    start_time = time.ticks_us()
    
    while ultrasonic_1_echo.value() == 1:
        pass
    end_time = time.ticks_us()
    
    # Calculate the distance in centimeters
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    
    return distance

def measure_distance_2():

    ultrasonic_2_echo = Pin(10, Pin.IN)
    ultrasonic_2_trigger = Pin(11, Pin.OUT)
    
    # Set trigger pin to low for 2 microseconds
    ultrasonic_2_trigger.low()
    time.sleep_us(2)
    
    # Send a 10-microsecond pulse to the trigger pin
    ultrasonic_2_trigger.high()
    time.sleep_us(10)
    ultrasonic_2_trigger.low()
    
    # Measure the duration of the echo pulse
    while ultrasonic_2_echo.value() == 0:
        pass
    start_time = time.ticks_us()
    
    while ultrasonic_2_echo.value() == 1:
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
    
    