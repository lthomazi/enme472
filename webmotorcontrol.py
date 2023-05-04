# This code is to test hosting a webpage with the Pico W
import wifi
import socket
from machine import Pin

# led pin to test code for blink with javascript
controller1 = Pin(12, Pin.OUT)
controller2 = Pin(13, Pin.OUT)
controller3 = Pin(14, Pin.OUT)
controller4 = Pin(15, Pin.OUT)
motor_status = "Off"


# Contents of the webpage
def web_page():

    # Define html code, with LED state passed to the server using javascript
    html = """
    <html><head><title>Lean Green Cleaning Machine</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>
        html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 2vh;}
        p{font-size: 1.5rem;}
        .button1{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white;
                         padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
        .button2{display: inline-block; background-color: #4286f4; border: none; border-radius: 4px; color: white;
                         padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
        .button2{display: inline-block; background-color:#fcba03; border: none; border-radius: 4px; color: white;
                         padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}                 
        </style>

        <script>
        <!-- function name -->
        function move_right() {
        <!-- message sent to server -->
            fetch("/move_right");
        <!-- log message on web client -->
            console.log("move right");
        <!-- run other function -->
            update_state();
        }
        </script>

        <script>
        function move_left() {
            fetch("/move_left");
            console.log("move left");
            update_state();
        }
        </script>

        <script>
        function stop_motor() {
            fetch("/stop_motor");
            console.log("stop motor");
            update_state();
        }
        </script>

        <script>
        function update_state() {

            fetch("/motor_status")
                .then(response => response.text())
                .then(state => {
                    document.getElementById("motor_status").innerHTML = state;
                });
        }
        </script>

        </head>
        <body onload="update_state();">
        <p>Motor Control</p>
        <p id="motor_status"></p>
        <button class="button1" onclick="move_left()"> Left </button>
        <button class="button2" onclick="move_right()"> Right </button>
        <button class="button" onclick="stop_motor()"> STOP </button>
        </body>
    </html>
    """
    return bytes(html, 'utf-16')

def move_right():
        controller1.on() 
        controller2.off()
        motor_status = "Moving Right"
        print(motor_status)

def move_left():
        controller1.on() 
        controller2.off() 
        motor_status = "Moving Left"
        print(motor_status)

def stop_all():
        controller1.off()
        controller2.off()
        controller3.off()
        controller4.off()
        motor_status = "Moving Stopped"
        print(motor_status)

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
            print('Waiting for connection...')
            try:
                conn, addr = s.accept()                 # blocking call -- code pauses until connected to client
                print(f'Connection from {addr}')
                
                # Recieve data from client
                request_data = conn.recv(1024)
                #print(request_data)

                # Process request
                if b"GET /move_right" in request_data:
                    # Move right
                    move_right()
                    response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nMotor moving right"
                    conn.send(response.encode("utf-16"))
                    conn.close()

                # Process request
                if b"GET /move_left" in request_data:
                    # Move left
                    move_left()
                    response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nMotor moving left"
                    conn.send(response.encode("utf-16"))
                    conn.close()

                # Process request
                if b"GET /stop_motor" in request_data:
                    # Stop Motor
                    stop_all()
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
                




if __name__ == "__main__":
        main()
