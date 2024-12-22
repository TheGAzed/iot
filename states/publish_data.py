from .state import AbstractState
from .sleep import Sleep
from .error import Error
from umqtt.simple import MQTTClient, MQTTException
import json, time, os, network

from boot import *

class Publish(AbstractState) :
    NAME = 'Publish Data'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        try:
            #mqtt = self.device.config['mqtt']
            mqtt = {
                "client"   : DEVICE_NAME,
                "server"   : self.device.wlan.ifconfig()[2],
                "port"     : 1883,
                "user"     : "maker",
                "password" : "this.is.mqtt",
            }
            
            client = MQTTClient(mqtt['client'], mqtt['server'], mqtt['port'], mqtt['user'], mqtt['password'])
            client.connect()
        
            with open(MEASUREMENTS_FILE, 'r') as file:
                data = json.load(file)['data']
                for d in data :
                    metric = { 'dt' : d['dt'], 'name' : d['name'], 'value' : d['value'], 'units' : d['units'] }
                    measure = { 'dt' : self.device.to_iso8601(time.time()), 'metrics' : [metric]}
                    client.publish('gw/' + d['name'] + '/' + DEVICE_NAME, json.dumps(measure))
                
                file.close()
        
            with open(MEASUREMENTS_FILE, 'w') as file:
                json.dump(DEFAULT_MEASUREMENTS, file)
                file.close()
            
            client.disconnect()
            self.device.wlan.deinit()
                        
            self.device.change_state(Sleep(self.device))
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))
