from machine import Pin, PWM
from time import sleep

#adds code

IN1 = Pin(12, Pin.OUT)
IN2 = Pin(13, Pin.OUT)

speed = PWM(Pin(10))
speed.freq(1000)

while True:
    for i in range(65535):
        speed.duty_u16(i)
        IN1.low()  #spin forward
        IN2.high()
   
    sleep(5)    
    IN1.low()  #stop
    IN2.low()
    sleep(2)
        

