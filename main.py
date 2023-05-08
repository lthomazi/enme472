''' 
This is code for controlling our robot. The code will have to:
    - control two motors
    - control solenoid valves for water control
    - measure distance of two ultrasonic sensors
'''

import machine
from time import sleep, sleep_us, ticks_us, ticks_diff
from machine import Pin, PWM, ADC
import _thread as thread
import wifi
import socket

led = Pin("LED", Pin.OUT)

# Threashold to be considered a gap (in cm)
GAP_DISTANCE = 5

# Ultrasonic sensor pins
ultrasonic_1_echo = Pin(7, Pin.IN)
ultrasonic_1_trigger = Pin(8, Pin.OUT)
ultrasonic_2_echo = Pin(9, Pin.IN)
ultrasonic_2_trigger = Pin(10, Pin.OUT)

# motor control pins
motor_speed1 = PWM(Pin(16))
motor1A = Pin(17, Pin.OUT)
motor1B = Pin(18, Pin.OUT)
motor2A = Pin(19, Pin.OUT)
motor2B = Pin(20, Pin.OUT)

# Solenoid control pins
solenoid = Pin(22, Pin.OUT)
solenoid.value(0)

# main function
def main():
    led.off()
    abortALL() # start the code without anything moving
    measure_distance_1()
    measure_distance_2()
    blink_led(3)

    gap_count = 0 # number of gaps between panels
    over_gap = False
    # "VOID LOOP"
    #while True:   
    status = 0 # 0 -> stop, 1 -> run, -1 -> reverse

    # forward
    status = 1
    motor1_forward()
    open_solenoid()
    motor2_on()
    
    # stop
    while True:
        d1 = measure_distance_1()
        d2 = measure_distance_2()
        if status == 1 and d1 > GAP_DISTANCE and d2 > GAP_DISTANCE:
            #print("OVER THE EDGE")
            abortALL()
            led.on()
            # reverse
            motor1_reverse()
            sleep(6)
            status = -1
            
            
        if status == -1 and measure_distance_2() > GAP_DISTANCE:
            sleep(1)
            abortALL()
                
                #print("END")
        
        sleep(0.2)
            

    

# blink led x times
def blink_led(x):
    led = Pin("LED", Pin.OUT)
    for i in range(x):
        led.on()
        sleep(1)
        led.off()
        sleep(1)
    

    


# Stop moving, stop water, stop brush
def abortALL():
    print("ABORT ALL")
    motor1_off()
    motor2_off()
    close_solenoid()

# Move forward
def motor1_forward():
    print("Motor 1 Running")
    for i in range(65535):
        motor_speed1.duty_u16(i)
        motor1A.low()
        motor1B.high()

# Move back
def motor1_reverse():
    for i in range(65535):
        motor_speed1.duty_u16(i)
        motor1A.high()
        motor1B.low()

# Stop moving
def motor1_off():
    motor1A.low()
    motor1B.low()

# Start brush
def motor2_on():
    print("Brush on")
    motor2A.low()
    motor2B.high()

# Stop brush
def motor2_off():
    motor2A.low()
    motor2B.low()


# Open or close solenoid
def open_solenoid():
    solenoid.on()

def close_solenoid():
    solenoid.off()

# Function to calculate the distance using ultrasonic sensor (HC-SR04)
def measure_distance_1():

    # Set trigger pin to low for 2 microseconds
    ultrasonic_1_trigger.low()
    sleep_us(2)
    
    # Send a 10-microsecond pulse to the trigger pin
    ultrasonic_1_trigger.high()
    sleep_us(10)
    ultrasonic_1_trigger.low()
    
    # Measure the duration of the echo pulse
    while ultrasonic_1_echo.value() == 0:
        pass
    start_time = ticks_us()
    
    while ultrasonic_1_echo.value() == 1:
        pass
    end_time = ticks_us()
    
    # Calculate the distance in centimeters
    duration = ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    #print("Distance 1: ", distance)
    return distance

def measure_distance_2():

    # Set trigger pin to low for 2 microseconds
    ultrasonic_2_trigger.low()
    sleep_us(2)
    
    # Send a 10-microsecond pulse to the trigger pin
    ultrasonic_2_trigger.high()
    sleep_us(10)
    ultrasonic_2_trigger.low()
    
    # Measure the duration of the echo pulse
    while ultrasonic_2_echo.value() == 0:
        pass
    start_time = ticks_us()
    
    while ultrasonic_2_echo.value() == 1:
        pass
    end_time = ticks_us()
    
    # Calculate the distance in centimeters
    duration = ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    #print("Distance 2: ", distance)
    return distance


if __name__ == '__main__':
    main()
    
    

