import time
import machine
from .state import AbstractState
from .error import Error

class Sleep(AbstractState) :
    NAME = 'Sleep'
    SLEEP_PERIOD_S = 10 * 60 # 10 minutes
    WDT_MS = 8388
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        try:
            time.sleep(self.SLEEP_PERIOD_S)
            self.device.initial_state()
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))        