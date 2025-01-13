from machine import Pin
import uasyncio

class Light() :
    BLINK_SLEEP_MS = 500

    BLINK = None
    
    def __init__(self, pin=None) :
        self.led = Pin("LED", Pin.OUT) if pin is None else pin
        self.led.off()
        
    async def blink(self) :
        while True :
            self.led.toggle()
            await uasyncio.sleep_ms(self.BLINK_SLEEP_MS)
