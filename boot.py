VERSION = 1.0

DEVICE_NAME = "zen-e6614103e7698839"

MAX_ERRORS = 5
WDT_MS = 20_000
WORK_FREQUENCY  = 100_000_000
SLEEP_FREQUENCY = 18_000_000

SLEEP_ERROR_S   =  5 * 60 #  5 minutes

SOUND_ADC = 0
PHOTO_ADC = 1

THP_SDA_PIN = 16
THP_SDL_PIN = 17

BUTTON_PIN = 20

CONFIG_FILE       = 'config.json'
MEASUREMENTS_FILE = 'measure.json'

DEFAULT_CONFIG = {
    "username" : "kronos-things",
    "password" : "welcome.to.the.kronos",
    "units"    : "metric",
    "time"     : {
        "start" : { "hour" :  0, "minute" :  0 },
        "end"   : { "hour" : 23, "minute" : 59 },
        "sleep_s" : 600
    }
}

DEFAULT_MEASUREMENTS = {
    "data" : []
}
