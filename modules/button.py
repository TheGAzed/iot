from machine import Pin, reset
import time

from boot import *

def handler(pin) :
    led = Pin("LED", Pin.OUT)
    led.on()
    deadline = time.ticks_add(time.ticks_ms(), 3000)
    while time.ticks_diff(deadline, time.ticks_ms()) > 0:
        if pin.value() == 0 :
            led.off()
            return
        
    led.off()
    reset()
        
class Button() :
    def __init__(self, pin):
        self.pin = pin
        
    def activate(self) :
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=handler)
    
    def deactivate(self) :
        self.pin.irq(handler=None)
        
