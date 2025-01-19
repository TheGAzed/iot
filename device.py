from machine import Pin, I2C, ADC
from states.init import Init
from states.state import AbstractState

import time, machine
from modules import thp, sound, photo, button, light

from boot import *

class Device() :
    def __init__(self) :
        print('>> Init device')
        
        self.thp    = thp.Thp(I2C(0, sda=Pin(THP_SDA_PIN), scl=Pin(THP_SDL_PIN)))
        self.sound  = sound.Sound(ADC(SOUND_ADC))
        self.photo  = photo.Photo(ADC(PHOTO_ADC))
        self.button = button.Button(Pin(BUTTON_PIN, Pin.IN))
        self.light  = light.Light()
        self.wlan   = None
        self.wdt    = None
        
        self.button.activate()

        self.config = dict()
        
        self.exception = ''
        
        self.initial_state()
        
    def to_iso8601(self, ts: int = 0) -> str:
        dt = time.gmtime(ts)
        return f'{dt[0]:04}-{dt[1]:02}-{dt[2]:02}T{dt[3]:02}:{dt[4]:02}:{dt[5]:02}Z'
        
    def run(self) :
        print('>> Run device')
        
        machine.freq(WORK_FREQUENCY)
        while (True) :
            self.state.enter()
            self.state.exec()
            self.state.exit()
        
    def change_state(self, state) :
        self.state = state
    
    def initial_state(self) :
        self.state = Init(self)
        
    def reset(self) :        
        self.thp    = thp.Thp(I2C(0, sda=Pin(THP_SDA_PIN), scl=Pin(THP_SDL_PIN)))
        self.sound  = sound.Sound(ADC(SOUND_ADC))
        self.photo  = photo.Photo(ADC(PHOTO_ADC))
        self.button = button.Button(Pin(BUTTON_PIN, Pin.IN))
        self.light  = light.Light()
        
        self.config = dict()
        self.exception = ''
        