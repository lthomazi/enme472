import time
import machine

# Function to calculate the distance using HC-SR04
def measure_distance(trigger_pin, echo_pin, timeout=1000000):
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
    
    # Initialize timeout counters
    start_counter = 0
    end_counter = 0
    
    # Measure the duration of the echo pulse
    while echo.value() == 0:
        start_counter += 1
        if start_counter > timeout:
            return None
        pass
    start_time = time.ticks_us()
    
    while echo.value() == 1:
        end_counter += 1
        if end_counter > timeout:
            return None
        pass
    end_time = time.ticks_us()
    
    # Calculate the distance in centimeters
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    
    return distance

# Define the GPIO pins for trigger and echo
trigger_pin = 2
echo_pin = 3

while True:
    # Measure and print the distance
    distance = measure_distance(trigger_pin, echo_pin)
    if distance is not None:
        print("Distance:", distance, "cm")
    else:
        print("Measurement timeout, trying again...")
    
    # Wait for 1 second before taking the next measurement
    time.sleep(0.1)

