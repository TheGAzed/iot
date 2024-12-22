from .state import AbstractState
from .error import Error
#from .receive_data import Receive
from .publish_data import Publish
import network, ntptime, time

class ConnectToWifi(AbstractState) :
    NAME = 'Connect To Wifi'
    DEFAULT_NETWORK = None
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def do_connect(self, ssid, key):
        self.device.wlan.active(True)
        for i in range(3) :
            print(f'Connecting to {ssid}')
            self.device.wlan.connect(ssid, key)
                
            deadline = time.ticks_add(time.ticks_ms(), 5000)
            while time.ticks_diff(deadline, time.ticks_ms()) > 0:
                if (self.device.wlan.isconnected()) :
                    return
                    
    def exec(self) :
        try:
            if self.DEFAULT_NETWORK != None :
                self.do_connect(self.DEFAULT_NETWORK + "-things", "welcome.to.the." + self.DEFAULT_NETWORK)
                
                if not self.device.wlan.isconnected() :
                    self.DEFAULT_NETWORK = None
                    for w in self.device.config['wifi']:
                        self.do_connect(w + "-things", "welcome.to.the." + w)
            else :
                for w in self.device.config['wifi']:
                    self.do_connect(w + "-things", "welcome.to.the." + w)
                    if self.device.wlan.isconnected() :
                        self.DEFAULT_NETWORK = w
                        break
                    
            if not self.device.wlan.isconnected() :
                raise Exception("Failed to connect to wifi.")
        
            #ntptime.host
            #ntptime.settime()
            self.device.change_state(Publish(self.device))
        
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))
            
            