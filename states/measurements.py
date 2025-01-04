from .state import AbstractState
from .error import Error
from .publish_data import Publish
import json, time
from time import sleep

from boot import *

class Measurement(AbstractState) :
    NAME = 'Measurement'
    
    def enter(self) :
        self.print()
        
    def exit(self) :
        pass
    
    def measure_thp(self) :
        self.device.thp.measure()
            
        self.measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "temperature", "value" : round(self.device.thp.temperature, 1), 'units' : 'celsius',
        })
        self.measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "humidity", "value" : round(self.device.thp.humidity, 1), 'units' : 'percent',
        })
        self.measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "pressure", "value" : round(self.device.thp.pressure, 1), 'units' : 'pascal',
        })
    
    def measure_sound(self) :
        self.device.sound.measure()
        
        self.measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "sound", "value" : round(self.device.sound.decibels, 1), 'units' : 'decibel',
        })
    
    def measure_luminosity(self) :
        self.device.photo.measure()
        
        self.measure['data'].append({
            "dt" : self.device.to_iso8601(time.time()), "name" : "luminosity", "value" : round(self.device.photo.luminosity, 1), 'units' : 'percent',
        })        
    
    def exec(self) :
        try:
            with open(MEASUREMENTS_FILE, 'r') as file:
                self.measure = json.load(file)
                file.close()
        except Exception as e:
            print(e)
            print('Creating new measurements file.')
            
            self.measure = DEFAULT_MEASUREMENTS
        
        try:
            self.measure_thp()
            self.measure_sound()
            self.measure_luminosity()
            
            with open(MEASUREMENTS_FILE, 'w') as file:
                json.dump(self.measure, file)
                file.close()

            self.device.change_state(Publish(self.device))
        except Exception as e:
            self.device.change_state(Error(self.device))
        
