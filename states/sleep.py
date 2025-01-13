import time, machine
from .state import AbstractState

from boot import *

class Sleep(AbstractState) :
    NAME = 'Sleep'
    
    def enter(self) :
        self.device.light.led.off()
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        machine.freq(SLEEP_FREQUENCY)
        time.sleep(SLEEP_PERIOD_S)
        machine.freq(WORK_FREQUENCY)

        self.device.initial_state()
     