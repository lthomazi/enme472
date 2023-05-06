''' 
This is code for controlling our robot. The code will have to:
    - control two motors
    - control solenoid valves for water control
    - measure distance of two ultrasonic sensors
'''

import machine
from time import time, sleep, sleep_us
from machine import Pin, PWM, ADC
import _thread as thread
import wifi
import socket

# Threashold to be considered a gap (in cm)
GAP_DISTANCE = 15

# Ultrasonic sensor pins
ultrasonic_1_echo = Pin(7, Pin.IN)
ultrasonic_1_trigger = Pin(8, Pin.OUT)
ultrasonic_2_echo = Pin(9, Pin.IN)
ultrasonic_2_trigger = Pin(10, Pin.OUT)

# motor control pins
motor_speed1 = PWM(Pin(15))
motor1A = Pin(14, Pin.OUT)
motor1B = Pin(13, Pin.OUT)
motor2A = Pin(12, Pin.OUT)
motor2B = Pin(11, Pin.OUT)

# Solenoid control pins
solenoid = Pin(22, Pin.OUT)
solenoid.value(0)

# main function
def main():
    abortALL() # start the code without anything moving

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

    gap_count = 0 # number of gaps between panels
    over_gap = False
    status = 0 # 0 -> stop, 1 -> run, -1 -> reverse
    # "VOID LOOP"
    while True:
        print('Waiting for connection...')
        
        
        try:
            global conn # global to be able to interupt movent on "abort" click
            conn, addr = s.accept()                 # blocking call -- code pauses until connected to client
            #print(f'Connection from {addr}')
            
            # Recieve data from client
            request_data = conn.recv(1024)
            #print(request_data)
            
            # END RIGHT: reaches the end on the right
            if status == 1 and measure_distance_1() > GAP_DISTANCE and measure_distance_2() > GAP_DISTANCE:
                motor2_off() # turn off brush
                close_solenoid() # turn off water
                motor1_reverse()
        
            # Forward: count the number of gaps while going forward if not over a gap already 
            if status == 1 and measure_distance_1() > GAP_DISTANCE and over_gap == False:
                over_gap = True
                gap_count += 1

            # reset over_gap if not over a gap anymore
            if over_gap == True and measure_distance_1() < GAP_DISTANCE:
                over_gap = False

            # Backward: count the number of gaps it went over
            if status == -1 and measure_distance_2() > GAP_DISTANCE and over_gap == False:
                over_gap = True
                gap_count -= 1

            # STOP BACK: 
            if status == -1 and gap_count == 0 and measure_distance_2() < GAP_DISTANCE:
                abortALL()


            # RECIEVE request
            if b"GET /run" in request_data:
                status = 1
                motor1_forward()
                motor2_on() # brush on
                open_solenoid() # open water
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nRunning"
                conn.send(response.encode("utf-16"))
                conn.close()

                

            # RECIEVE request
            if b"GET /abort" in request_data:
                # Stop Motor
                abortALL()
                status = 0
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nAborted"
                conn.send(response.encode("utf-16"))
                conn.close()
            
            # RECIEVE request
            if b"GET /reset" in request_data:
                motor2_off()        # turn off brush
                water_off() # turn water off
                motor1_reverse()    # move motor back
                status = -1
            

                motor1_off()
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nResetting"
                conn.send(response.encode("utf-16"))
                conn.close()
            
            # RECIEVE request
            if b"GET /brush_on" in request_data:
                motor2_on()
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nBrush On"
                conn.send(response.encode("utf-16"))
                conn.close()

            # SEND motor status
            if b"GET /status" in request_data:
                response = f"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n{status}"
                conn.send(response.encode("utf-16"))
                conn.close()

            # Only send the HTML page when the path is /
            if b"GET / " in request_data:
                conn.send('HTTP/1.0 200 OK\n')
                conn.send('Content-type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(web_page())
                conn.close()
    # -----------------END OF VOID LOOP-----------------------------------------------    

        except OSError as e:
            conn.close()
            print('connection closed')

# Web page content
def web_page():
    with open("index.html", "r", encoding="utf-8") as file:
        html = file.read()
    return bytes(html, 'utf-16')

# Stop moving, stop water, stop brush
def abortALL():
    motor1_off()
    motor2_off()
    close_solenoid()

# Move forward
def motor1_forward():
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
    # Check for if abort button is pressed while measuring distance
    # Recieve data from client
    request_data = conn.recv(1024)
    # Process request
    if b"GET /abort" in request_data:
        # Stop Motor
        abortALL()
        response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nMotor stopped"
        conn.send(response.encode("utf-16"))
        conn.close()

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
    start_time = time.ticks_us()
    
    while ultrasonic_1_echo.value() == 1:
        pass
    end_time = time.ticks_us()
    
    # Calculate the distance in centimeters
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    
    return distance

def measure_distance_2():
    # Check for if abort button is pressed while measuring distance
    # Recieve data from client
    request_data = conn.recv(1024)
    # Process request
    if b"GET /abort" in request_data:
        # Stop Motor
        abortALL()
        response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nMotor stopped"
        conn.send(response.encode("utf-16"))
        conn.close()

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
    start_time = time.ticks_us()
    
    while ultrasonic_2_echo.value() == 1:
        pass
    end_time = time.ticks_us()
    
    # Calculate the distance in centimeters
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    
    return distance


if __name__ == '__main__':
    main()
    
    