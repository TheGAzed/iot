from .state import AbstractState
from .error import Error
from .measurements import Measurement
import network, ntptime, time

class ConnectToWifi(AbstractState) :
    NAME = 'Connect To Wifi'
    DEFAULT_SSID = None
    DEFAULT_PASSWORD = None
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def do_connect(self, ssid, key):
        for i in range(3) :
            print(f'Connecting to {ssid}.')
            self.device.wlan.connect(ssid, key)
                
            deadline = time.ticks_add(time.ticks_ms(), 5000)
            while time.ticks_diff(deadline, time.ticks_ms()) > 0:
                if (self.device.wlan.isconnected()) :
                    return
                
    def connect_gateway(self) :
        roomset = { "kronos", "abydoss", "caprica", "dune", "endor", "hyperion", "meridian", "romulus", "solaris", "vulkan" }
        for s in self.device.wlan.scan():
            ssid = s[0].decode('UTF-8')
            split = ssid.split("-")
                    
            if split[0] not in roomset or not ssid.endswith("-things"):
                continue
                    
            self.do_connect(ssid, "welcome.to.the." + split[0])
            if self.device.wlan.isconnected() :
                self.DEFAULT_SSID = ssid
                self.DEFAULT_PASSWORD = "welcome.to.the." + split[0]
                return
        
        raise Exception('Failed to find gateway network.')
        
                    
    def exec(self) :
        try:
            self.device.wlan = network.WLAN(network.STA_IF)
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))   

        try:
            self.device.wlan = network.WLAN(network.STA_IF)
            self.device.wlan.active(True)
            
            if self.DEFAULT_SSID != None and  self.DEFAULT_PASSWORD != None:
                self.do_connect(self.DEFAULT_SSID, self.DEFAULT_PASSWORD)
                
                if not self.device.wlan.isconnected() :
                    self.connect_gateway()
            else :
                self.connect_gateway()
                    
            ntptime.host
            ntptime.settime()
            self.device.change_state(Measurement(self.device))
        except Exception as e:
            self.device.wlan.deinit()
            self.device.exception = e
            self.device.change_state(Error(self.device))
            