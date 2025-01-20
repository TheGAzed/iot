from .state import AbstractState
from .error import Error
from .measurements import Measurement
from .sleep import Sleep
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
        
        raise Exception('Failed to connect to network.')
        
    def ntp_connect(self) :
        try:
            ntptime.host
            ntptime.settime()
        except Exception as e:
            raise Exception('Failed to connect to NTP server.')
        
    def wlan_connect(self) :
        self.device.wlan = network.WLAN(network.STA_IF)
        self.device.wlan.active(True)

        self.do_connect(self.device.config['username'], self.device.config['password'])
                    
    def exec(self) :
        try:
            self.wlan_connect()
            self.ntp_connect()

            lt = time.localtime()

            h = lt[3]
            m = lt[4]

            sh = self.device.config['time']['start']['hour']
            sm = self.device.config['time']['start']['minute']

            eh = self.device.config['time']['end']['hour']
            em = self.device.config['time']['end']['minute']

            if (sh <= h <= eh) and (sm <= m <= em) :
                self.device.change_state(Measurement(self.device))
            else :
                self.device.wlan.deinit()
                self.device.change_state(Sleep(self.device))

        except Exception as e:
            self.device.wlan.deinit()
            self.device.exception = e
            self.device.change_state(Error(self.device))
            