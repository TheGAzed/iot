from .state import AbstractState
from .error import Error
from .publish_data import Publish
import json, time

from boot import *

class Measurement(AbstractState) :
    NAME = 'Measurement'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass

    def measure_signal(self, measure : dict) :
        measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "rssi", "value" : self.device.wlan.status('rssi'), 'units' : 'decibel-milliwatts',
        })

    def measure_thp(self, measure : dict) :
        self.device.thp.measure()
            
        measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "temperature", "value" : round(self.device.thp.temperature, 1), 'units' : 'celsius',
        })
        measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "humidity", "value" : round(self.device.thp.humidity, 1), 'units' : 'percent',
        })
        measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "pressure", "value" : round(self.device.thp.pressure, 1), 'units' : 'pascal',
        })
    
    def measure_sound(self, measure) :
        self.device.sound.measure()
        
        measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "sound", "value" : round(self.device.sound.decibels, 1), 'units' : 'decibel',
        })
    
    def measure_luminosity(self, measure) :
        self.device.photo.measure()
        
        measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "light", "value" : round(self.device.photo.luminosity, 1), 'units' : 'percent',
        })        
    
    def exec(self) :
        measure = None

        try:
            with open(MEASUREMENTS_FILE, 'r') as file:
                measure = json.load(file)
                file.close()
        except Exception as e:
            print(e)
            print('Creating new measurements file.')
            
            measure = DEFAULT_MEASUREMENTS
        
        try:
            self.measure_thp(measure)
            self.measure_sound(measure)
            self.measure_luminosity(measure)
            self.measure_signal(measure)
            
            with open(MEASUREMENTS_FILE, 'w') as file:
                json.dump(measure, file)
                file.close()

            self.device.change_state(Publish(self.device))
        except Exception as e:
            self.device.change_state(Error(self.device))
        
