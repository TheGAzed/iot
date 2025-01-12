from .state import AbstractState
from .sleep import Sleep
from .error import Error
from umqtt.simple import MQTTClient
import json, time, machine, urequests

from boot import *

def on_message(topic: bytes, message: bytes):
    print(f'Message "{message}" received in topic "{topic}"')

class Publish(AbstractState) :
    NAME = 'Publish Data'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass

    def on_message(self, topic: bytes, message: bytes):
        print(f'Message "{message}" received in topic "{topic}"')
        cmd = json.load(message)
            
        if cmd['version'] > VERSION :
            print(">> Downloading update from {}".format(cmd['url']))
            response = urequests.get(cmd['url'])

            with open(cmd['file'], 'wb') as file:
                file.write(response.content)
                file.close()

            response.close()
                    
            machine.reset()

    def create_mqtt(self) :
        return {
            "client" : self.device.config['name'], "server" : self.device.wlan.ifconfig()[2],
            "port" : 1883, "user" : "maker", "password" : "this.is.mqtt",
        }
    
    def subscribe(self, client) :
        client.subscribe('gateway/thing/' + client.client_id + '/set')
        time.sleep(1)
        client.check_msg()      
    
    def publish(self, client) :
        with open(MEASUREMENTS_FILE, 'r') as file:
            data = json.load(file)['data']
            for d in data :
                metric = { 'dt' : d['dt'], 'name' : d['name'], 'value' : d['value'], 'units' : d['units'] }
                measure = { 'dt' : self.device.to_iso8601(time.time()), 'metrics' : [metric]}
                client.publish('gateway/' + d['name'] + '/' + client.client_id, json.dumps(measure), retain=True, qos=1)
                
            file.close()

        with open(MEASUREMENTS_FILE, 'w') as file:
            json.dump(DEFAULT_MEASUREMENTS, file)
            file.close()

    def exec(self) :
        try:
            mqtt = self.create_mqtt()
            
            client = MQTTClient(mqtt['client'], mqtt['server'], mqtt['port'], mqtt['user'], mqtt['password'])
            client.set_callback(self.on_message)

            client.connect()

            self.subscribe(client)

            self.publish(client)
            
            client.disconnect()
            self.device.wlan.active(False)
            self.device.wlan.deinit()
                        
            self.device.change_state(Sleep(self.device))
        except Exception as e:
            self.device.wlan.active(False)
            self.device.wlan.deinit()
            self.device.exception = e
            self.device.change_state(Error(self.device))
