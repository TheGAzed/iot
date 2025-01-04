from .state import AbstractState
from .connect_to_wifi import ConnectToWifi
from .error import Error
import time, json, network

from boot import *

class Init(AbstractState) :
    NAME = 'Init'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        try:
            self.device.wlan = network.WLAN(network.STA_IF)
        except Exception as e:
            self.device.change_state(Error(self.device))
            
        try:
            #self.device.wdt  = WDT(timeout=8000)            
            with open(CONFIG_FILE, 'r') as file:
                self.device.config = json.load(file)
                file.close()
        except Exception as e:
            print('Error: Config file not found. Creating default one.')
            with open(CONFIG_FILE, 'w') as file:
                file.write(json.dumps(DEFAULT_CONFIG))
                file.close()
                
            self.device.config = DEFAULT_CONFIG
        
        self.device.change_state(ConnectToWifi(self.device))
