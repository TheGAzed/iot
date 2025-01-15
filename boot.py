VERSION = 1.0

DEVICE_NAME = "zen-e6614103e7698839"

WORK_FREQUENCY  = 100_000_000
SLEEP_FREQUENCY = 18_000_000

SLEEP_SUCCESS_S = 10 * 60 # 10 minutes
SLEEP_ERROR_S   =  5 * 60 #  5 minutes

SOUND_ADC = 0
PHOTO_ADC = 1

THP_SDA_PIN = 16
THP_SDL_PIN = 17

BUTTON_PIN = 20

CONFIG_FILE       = 'config.json'
MEASUREMENTS_FILE = 'measure.json'

DEFAULT_CONFIG = {
    "units" : "metric"
}

DEFAULT_MEASUREMENTS = {
    "data" : [],
}
