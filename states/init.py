from .state import AbstractState
from .self_test import SelfTest
from .error import Error
import json
import machine

from boot import *

def wdt_callback(timer) :
    timer.deinit()
    machine.reset()

class Init(AbstractState) :
    NAME = 'Init'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass

    def wdt(self) :
        try:
            self.device.wdt = machine.Timer()
            self.device.wdt.init(mode=machine.Timer.ONE_SHOT, period=WDT_MS, callback=wdt_callback)
        except:
            raise Exception('Failed initialize watchdog timer.')
    
    def config(self) :
        try:
            with open(CONFIG_FILE, 'r') as file:
                self.device.config = json.load(file)
                file.close()
        except:
            print('Error: Config file not found. Creating default one.')
            with open(CONFIG_FILE, 'w') as file:
                file.write(json.dumps(DEFAULT_CONFIG))
                file.close()
                
            self.device.config = DEFAULT_CONFIG
        
    def exec(self) :
        try:
            self.wdt()
            self.config()
        except:
            self.device.change_state(Error(self.device))

        self.device.change_state(SelfTest(self.device))
