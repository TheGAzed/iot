import sys, network, time
from .state import AbstractState

from boot import *
class Sleep(AbstractState) :
    NAME = 'Sleep'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        time.sleep(SLEEP_PERIOD_S)
        self.device.reset_state()
        