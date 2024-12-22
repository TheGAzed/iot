from .state import AbstractState
from .sleep import Sleep
from time import sleep
import uasyncio, machine

class Error(AbstractState) :
    NAME = 'Error'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        self.device.deactivate()
        print(self.device.exception)
        
        uasyncio.run(self.device.light.blink())
        self.device.change_state(Sleep(self.device))
        #machine.deepsleep()
        