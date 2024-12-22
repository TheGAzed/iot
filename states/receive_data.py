from .state import AbstractState
from .publish_data import Publish
from .error import Error
from umqtt.simple import MQTTClient, MQTTException
import json, sys

from boot import *

def on_message(topic, message) :
    try:
        msg = json.loads(message.decode("utf-8"))
            
        if ('cmd' in msg) :
            if (msg['cmd'] == "shutdown") :
                sys.exit(0)
            elif (msg['cmd'] == "update") :
                pass
        elif ('status' in msg) :
            if (msg['status'] == "offline") :
                pass
            elif (msg['status'] == "online") :
                pass
        else :
            raise Exception("Invalid message key.")
    except Exception as e:
        self.device.exception = e
        self.device.change_state(Error(self.device))
            
class Receive(AbstractState) :
    NAME = 'Receive Data'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def exec(self) :
        try:
            mqtt = self.device.config['mqtt']
            
            client = MQTTClient(mqtt['client_id'], mqtt['server'], mqtt['port'], mqtt['user'], mqtt['password'])
            client.set_callback(on_message)
            
            client.subscribe('services/notifier/' + DEVICE_NAME + '/cmd')
            
            client.connect()
        
            client.disconnect()
                        
            self.device.change_state(Publish(self.device))
        except Exception as e:
            self.device.exception = e
            self.device.change_state(Error(self.device))

