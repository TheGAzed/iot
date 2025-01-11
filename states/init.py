from .state import AbstractState
from .connect_to_wifi import ConnectToWifi
from .error import Error
import json, network

from boot import *

class Init(AbstractState) :
    NAME = 'Init'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
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
        
        self.device.change_state(ConnectToWifi(self.device))
