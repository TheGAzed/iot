from machine import Pin, reset, freq
import time

BUTTON_PRESS_MS = 3_000

from boot import *

def handler(pin) :
    freq(WORK_FREQUENCY)
    led = Pin("LED", Pin.OUT)
    led.on()
    deadline = time.ticks_add(time.ticks_ms(), BUTTON_PRESS_MS)
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
        
