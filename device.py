from machine import Pin, I2C, ADC, WDT
from states.self_test import SelfTest
from states.state import AbstractState
from time import gmtime

from modules import thp, sound, photo, button, light

from boot import *

class Device() :
    NAME = 'zen'
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
        
        self.state = SelfTest(self)
        
    def to_iso8601(self, ts: int = None) -> str:
        dt = gmtime(ts)
        return f'{dt[0]:04}-{dt[1]:02}-{dt[2]:02}T{dt[3]:02}:{dt[4]:02}:{dt[5]:02}Z'
        
    def run(self) :
        print('>> Run device')
        
        while (True) :
            self.state.enter()
            self.state.exec()
            self.state.exit()
    
    def deactivate(self) :
        #self.button.dectivate()
        if (self.wlan != None) :
            self.wlan.deinit()
        
    def change_state(self, state) :
        self.state = state
    
    def reset_state(self):
        self.change_state(SelfTest(self))
        
    def reset(self) :        
        self.thp    = thp.Thp(I2C(0, sda=Pin(THP_SDA_PIN), scl=Pin(THP_SDL_PIN)))
        self.sound  = sound.Sound(ADC(SOUND_ADC))
        self.photo  = photo.Photo(ADC(PHOTO_ADC))
        self.button = button.Button(Pin(BUTTON_PIN, Pin.IN))
        self.light  = light.Light()
        
        self.config = dict()
        self.exception = ''
        