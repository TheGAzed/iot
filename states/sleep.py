import time, machine
from .state import AbstractState
from .error import Error

from boot import *

class Sleep(AbstractState) :
    NAME = 'Sleep'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        self.device.wdt.deinit()
        try:            
            machine.freq(SLEEP_FREQUENCY)

            time.sleep(self.device.config['sleep'])

            machine.freq(WORK_FREQUENCY)

            self.device.errors = 0

            self.device.initial_state()
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))
     