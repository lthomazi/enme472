from machine import Pin, PWM
import time

controller1 = PWM(Pin(12))
controller2 = PWM(Pin(13))
controller3 = PWM(Pin(14))
controller4 = PWM(Pin(15))

# Turn motor connected to OUT1 & OUT2 on in one direction
#controller1.on()
#controller2.off()

# Turn motor connected to OUT1 & OUT2 on in other direction
#controller1.off()
#controller2.on()

# Turn motor connected to OUT3 & OUT4 on in one direction
#controller3.on()
#controller4.off()

# Turn motor connected to OUT3 & OUT4 on in other direction
#controller3.off()
#controller4.on()

controller1.duty(0)
controller2.duty(0)

for i in range(65535):
        controller1.duty_u16(i)
        controller2.duty(0)
        time.sleep(0.01)

controller1.duty(65535)
controller2.duty(0)

while True:
    pass
