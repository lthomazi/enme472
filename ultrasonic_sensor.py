import machine
import time

# Define the GPIO pins for the ultrasonic sensor
TRIG_PIN = machine.Pin(17, machine.Pin.OUT)
ECHO_PIN = machine.Pin(16, machine.Pin.IN)
led = machine.Pin("LED", machine.Pin.OUT)

# Function to measure distance
def measure_distance():
    # Set trigger pin to high for 10us
    TRIG_PIN.high()
    time.sleep_us(10)
    TRIG_PIN.low()

    # Wait for echo pin to go high
    while ECHO_PIN.value() == 0:
        pass
    start_time = time.ticks_us()

    # Wait for echo pin to go low
    while ECHO_PIN.value() == 1:
        pass
    end_time = time.ticks_us()

    # Calculate the distance in centimeters
    duration = end_time - start_time
    distance = duration / 58

    return distance

# Main loop
while True:
    #led.on()
    distance = measure_distance()
    print(distance)
    time.sleep(1)
    
    if distance > 15:
        led.on()
    else:
        led.off()
        
    time.sleep(0.1)

