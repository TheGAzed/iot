from .state import AbstractState
import uasyncio, machine
from .sleep import Sleep

class Error(AbstractState) :
    NAME = 'Error'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        print(self.device.exception)
        
        uasyncio.run(self.device.light.blink())
        self.device.change_state(Sleep(self.device))
        