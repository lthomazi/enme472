# This code is to test hosting a webpage with the Pico W

import wifi
import socket
from machine import Pin

# led pin to test code for blink via POST
led = Pin("LED", Pin.OUT)
web_data = ""

# Serve the web page to a client on connection
def serve_web_page():
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
   
        print('Waiting for connection...')
        conn, addr = s.accept()                 # connected to client
        print(f'Connection from {addr}')
        
        # Recieve data from client
        web_data = getPOSTdata(conn.recv(1024))    # specify buffer size (max data to be received)
        
        conn.send('HTTP/1.0 200 OK\n')          # status line 
        conn.send('Content-type: text/html\n')  # header (content type)
        conn.send('Connection: close\n\n')      # header (tell client to close at end)
        conn.sendall(web_page())                # body
        conn.close()

# Contents of the webpage
def web_page():
    if led.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"

    # Define html code, with GPIO state passed to the browser via POST request
    html = """
    <html><head><title>Web Server Test</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
    html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white;
                     padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}
    </style>
    </head>
    <body>
    <h1>Web Server Test</h1> 
    <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
    <form action="/" method="POST">
      <p><button type="submit" class="button" name="state" value="b_on">ON</button></p>
      <p><button type="submit" class="button button2" name="state" value="b_off">OFF</button></p>
    </form>
    </body>
    </html>
    """
    return bytes(html, 'utf-16')
    
# Returns a dictionary of {key:value} pairs from the message
def getPOSTdata(client_message):
    #print(client_message, '\n')
    data_dict = {}
    data = str(client_message)   # convert from bytes
    data = data[data.find('\\r\\n\\r\\n')+8 : -1]
    #print(data, '\n')
    data_pairs = data.split('&')
    #print(data_pairs, '\n')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
           
    return data_dict


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

        while True:
                serve_web_page()
                




if __name__ == "__main__":
        main()