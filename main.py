''' 
This is code for controlling our robot. The code will have to:
    - control two motors
    - control solenoid valves for water control
    - measure distance of two ultrasonic sensors
'''

import machine
from time import time, sleep
from machine import Pin, PWM, ADC
import _thread as thread

# Ultrasonic sensor pins
ultrasonic_1_echo = Pin(7, Pin.IN)
ultrasonic_1_trigger = Pin(8, Pin.OUT)
ultrasonic_2_echo = Pin(9, Pin.IN)
ultrasonic_2_trigger = Pin(10, Pin.OUT)

# motor control pins
motor_speed1 = PWM(Pin(11))
motor1A = Pin(12, Pin.OUT)
motor1B = Pin(13, Pin.OUT)
motor2A = Pin(14, Pin.OUT)
motor2B = Pin(15, Pin.OUT)

# Solenoid control pins
solenoid = Pin(22, Pin.OUT)

# main function
def main():
        pass

def abortALL():
    motor1_off()
    motor2_off()
    close_solenoid()

def motor1_forward():
    for i in range(65535):
        motor_speed1.duty_u16(i)
        motor1A.low()
        motor1B.high()

def motor1_reverse():
    for i in range(65535):
        motor_speed1.duty_u16(i)
        motor1A.high()
        motor1B.low()

def motor1_off():
    motor1A.low()
    motor1B.low()

def motor2_forward():
    motor2A.low()
    motor2B.high()

def motor2_off():
    motor2A.low()
    motor2B.low()


# solenoid-relay pins
solenoid = Pin(22,Pin.OUT)
solenoid.value(0)

# Open or close solenoid
def open_solenoid():
    solenoid.on()
    time.sleep(0.5)

def close_solenoid():
    solenoid.off()
    time.sleep(0.5)

# Function to calculate the distance using ultrasonic sensor (HC-SR04)
def measure_distance_1():
    
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
    
    