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
        self.device.wlan.connect(ssid, key)
        for i in range(3) :
            print(f'Connecting to {ssid}.')
                
            deadline = time.ticks_add(time.ticks_ms(), 5_000)
            while time.ticks_diff(deadline, time.ticks_ms()) > 0:
                if (self.device.wlan.isconnected()) :
                    return
        
        raise Exception('Failed to connect to network.')
    
    def connect_gateway(self) :
        roomset = { "kronos", "abydoss", "caprica", "dune", "endor", "hyperion", "meridian", "romulus", "solaris", "vulkan" }
        for s in self.device.wlan.scan():
            ssid = s[0].decode('UTF-8')
            split = ssid.split("-")
                    
            if split[0] not in roomset or not ssid.endswith("-things"):
                continue
                    
            self.do_connect(ssid, "welcome.to.the." + split[0])
            if self.device.wlan.isconnected() :
                return

        raise Exception('Failed to find gateway network.')
        
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

        if not self.device.wlan.isconnected() :
            self.connect_gateway()
                    
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
            