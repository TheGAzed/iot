from .state import AbstractState
from .sleep import Sleep
from .error import Error
from umqtt.simple import MQTTClient
import json, time, machine, urequests, ujson

from boot import *

class Publish(AbstractState) :
    NAME = 'Publish Data'
    COMMAND_UPDATE = 0
    COMMAND_CONFIG = 1
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass

    def on_message(self, topic: bytes, message: bytes):
        print(f'Message "{message}" received in topic "{topic}"')
        msg = ujson.loads(message.decode("utf-8"))

        cmd  = msg['command']
        args = msg['arguments']

        if cmd == self.COMMAND_UPDATE :
            print(">> Downloading update from {}".format(args['url']))
            response = urequests.get(args['url'])

            with open(args['file'], 'wb') as file:
                file.write(response.content)
                file.close()

            response.close()

            machine.reset()
        elif cmd == self.COMMAND_CONFIG :
            for a in args.keys() :
                self.device.config[a] = args[a]
            
            with open(CONFIG_FILE, 'w') as file:
                file.write(json.dumps(self.device.config))
                file.close()

    def create_mqtt(self) :
        gateway_ip = self.device.wlan.ifconfig()[2]
        #print(gateway_ip)

        return {
            "client"   : DEVICE_NAME, 
            "server"   : gateway_ip,
            "port"     : 1883, 
            "user"     : "maker", 
            "password" : "this.is.mqtt",
        }
    
    def subscribe(self, client : MQTTClient) :
        client.subscribe('gw/thing/' + client.client_id + '/set')
        time.sleep(5)
        client.check_msg()
    
    def publish(self, client : MQTTClient) :
        client.publish('gw/thing/' + client.client_id, json.dumps({ "ssid" : self.device.wlan.config('ssid')} ), retain=True)
        with open(MEASUREMENTS_FILE, 'r') as file:
            data = json.load(file)['data']
            for d in data :
                metric = { 'dt' : d['dt'], 'name' : d['name'], 'value' : d['value'], 'units' : d['units'] }
                measure = { 'dt' : self.device.to_iso8601(time.time()), 'metrics' : [metric]}
                client.publish('gw/' + d['name'] + '/' + client.client_id, json.dumps(measure), retain=True)
                
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
