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
    # Open the text file and read its contents
    with open("wifi_credentials.txt", "r") as f:
            content = f.read().splitlines()

    # Extract the SSID and password from the content
    network_name = content[0]
    password = content[1]
    # To access HTML page, connect to IP address via browser
    ip = wifi.connect(network_name, password)
    print(ip)
    # Set up Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # pass IP addr & socket type
    # AF_INET -> IPv4 socket
    # SOCK_STREAM -> use TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))     #  # Bind HOST IP address through the given PORT 
    # HOST can be a specific IP address, the loopback address (127.0.0.1), 
    # or an empty string (meaning any connection will be allowed). 
    # PORT can be a privileged port such as 80 for HTTP, or a custom port > 1023
    s.listen(5)          # up to 5 queued connections

    while True:
        status = 0 # 0 -> stop/abortALL, 1 -> motor1_forward, -1 -> motor1_reverse
        print('Waiting for connection...')
        try:
            conn, addr = s.accept()                 # blocking call -- code pauses until connected to client
            print(f'Connection from {addr}')
            
            # Recieve data from client
            request_data = conn.recv(1024)
            #print(request_data)

            # Process request
            if b"GET /run" in request_data:
                # TODO: Run robot autonomously
                while True:
                    pass
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nRunning"
                conn.send(response.encode("utf-16"))
                conn.close()

            # Process request
            if b"GET /stop_motor" in request_data:
                # Stop Motor
                abortALL()
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nMotor stopped"
                conn.send(response.encode("utf-16"))
                conn.close()
            
            # Update motor status
            if b"GET /motor_status" in request_data:
                response = f"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n{motor_status}"
                conn.send(response.encode("utf-16"))
                conn.close()

            # Only send the HTML page when the path is /
            if b"GET / " in request_data:
                conn.send('HTTP/1.0 200 OK\n')
                conn.send('Content-type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(web_page())
                conn.close()
        
#                print(motor_status) 

        except OSError as e:
            conn.close()
            print('connection closed')

 

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

def motor2_reverse():
    motor2A.high()
    motor2B.low()

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
    
    