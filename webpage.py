# This code is to test hosting a webpage with the Pico W

import wifi
import socket
from machine import Pin

# led pin to test code for blink with javascript
led = Pin("LED", Pin.OUT)
led.off()
led_state = "OFF"
web_data = ""


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
        </style>

        <script>
        function turnLEDOn() {
            fetch("/ledon");
            console.log("led on");
            updateLEDState();
        }
        </script>

        <script>
        function turnLEDOff() {
            fetch("/ledoff");
            console.log("led off");
            updateLEDState();
        }
        </script>

        <script>
        function updateLEDState() {
            fetch("/ledstate")
                .then(response => response.text())
                .then(state => {
                    document.getElementById("ledState").innerHTML = state;
                });
        }
        </script>

        </head>
        <body onload="updateLEDState();">
        <p>LED Switch</p>
        <p id="ledState"></p>
        <button class="button1" onclick="turnLEDOn()"> ON </button>
        <button class="button2" onclick="turnLEDOff()"> OFF </button>
        </body>
    </html>
    """
    return bytes(html, 'utf-16')


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
                print(request_data)

                # Process request
                if b"GET /ledon" in request_data:
                    # Turn the LED on
                    led.on()
                    response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nLED turned on"
                    conn.send(response.encode("utf-16"))
                    conn.close()

                # Process request
                if b"GET /ledoff" in request_data:
                    # Turn the LED on
                    led.off()
                    response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nLED turned off"
                    conn.send(response.encode("utf-16"))
                    conn.close()

                if b"GET /ledstate" in request_data:
                    led_state = "ON" if led.value() else "OFF"
                    response = f"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n{led_state}"
                    conn.send(response.encode("utf-16"))
                    conn.close()

                # Only send the HTML page when the path is /
                if b"GET / " in request_data:
                    conn.send('HTTP/1.0 200 OK\n')
                    conn.send('Content-type: text/html\n')
                    conn.send('Connection: close\n\n')
                    conn.sendall(web_page())
                    conn.close()
            

            except OSError as e:
                conn.close()
                print('connection closed')
                




if __name__ == "__main__":
        main()