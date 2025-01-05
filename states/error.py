from .state import AbstractState
import uasyncio, machine

class Error(AbstractState) :
    NAME = 'Error'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        print(self.device.exception)
        
        uasyncio.run(self.device.light.blink())
        machine.deepsleep()
        