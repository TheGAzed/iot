from .state import AbstractState
import uasyncio, time, machine, sys

from boot import *

class Error(AbstractState) :
    NAME = 'Error'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        self.device.errors += 1

        if self.device.errors == MAX_ERRORS :
            sys.exit("Maximum error count reached")
        
        self.device.wdt.deinit()
        print(self.device.exception)
        
        uasyncio.run(self.device.light.blink())
        machine.freq(SLEEP_FREQUENCY)

        time.sleep(SLEEP_ERROR_S)

        machine.freq(WORK_FREQUENCY)

        self.device.initial_state()
        