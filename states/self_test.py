from .state import AbstractState
from .connect_to_wifi import ConnectToWifi
from .error import Error

class SelfTest(AbstractState) :
    NAME = 'Self Test'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        try:
            self.device.thp.measure()
            
            if (self.device.thp.temperature < -40 or self.device.thp.temperature > 85) :
                raise Exception(f"Invalid temperature value = {self.device.thp.temperature}.")
                
            if (self.device.thp.humidity < 0 or self.device.thp.humidity > 100) :
                raise Exception(f"Invalid humidity value = {self.device.thp.humidity}.")
                
            if (self.device.thp.pressure < 30000 or self.device.thp.pressure > 110000) :
                raise Exception(f"Invalid pressure value = {self.device.thp.pressure}.")
                
            self.device.change_state(ConnectToWifi(self.device))
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))
