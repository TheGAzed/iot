import sys, network, time
from .state import AbstractState

class End(AbstractState) :
    NAME = 'End'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        self.is_running = False