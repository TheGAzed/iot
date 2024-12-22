from machine import Pin, ADC
#from time import sleep
import math, time

class Sound() :
    decibels = 0
    
    MIN_SIGNAL = const(0)
    MAX_SIGNAL = const(65536)
    SAMPLES_MS = const(100)
    
    MIN_DB = const(50)
    MAX_DB = const(110)
    
    def __map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    
    def measure(self) :
        signal_max = MIN_SIGNAL
        signal_min = MAX_SIGNAL
        
        deadline = time.ticks_add(time.ticks_ms(), SAMPLES_MS)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            sample = self.sensor.read_u16()
            if (sample < MAX_SIGNAL) :
                if (sample > signal_max) :
                    signal_max = sample
                elif (sample < signal_min) :
                    signal_min = sample
                        
        peakToPeak = signal_max - signal_min
        self.decibels = self.__map(peakToPeak, MIN_SIGNAL, MAX_SIGNAL, MIN_DB, MAX_DB)
    
    def __init__(self, adc) :
        self.sensor = adc
        