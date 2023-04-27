from machine import Pin
from time import sleep

def init():
    pins = [17, 18, 19, 20]
    for pin in pins:
        Pin(pin, Pin.OUT)

def forward(sec):
    init()
    Pin(17, Pin.OUT).on()
    Pin(18, Pin.OUT).off()
    Pin(19, Pin.OUT).on()
    Pin(20, Pin.OUT).off()
    sleep(sec)

def reverse(sec):
    init()
    Pin(17, Pin.OUT).off()
    Pin(18, Pin.OUT).on()
    Pin(19, Pin.OUT).off()
    Pin(20, Pin.OUT).on()
    sleep(sec)

print("forward")
forward(4)
print("reverse")
reverse(2)

