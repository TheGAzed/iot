from .state import AbstractState
import uasyncio, time, machine

from boot import *

class Error(AbstractState) :
    NAME = 'Error'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        self.device.wdt.deinit()
        print(self.device.exception)
        
        uasyncio.run(self.device.light.blink())
        machine.freq(SLEEP_FREQUENCY)

        time.sleep(SLEEP_ERROR_S)

        machine.reset()
        