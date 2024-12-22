DEVICE_NAME = 'zen-e6614103e7698839'
SLEEP_PERIOD_S = 5 * 60

SOUND_ADC = 0
PHOTO_ADC = 2

THP_SDA_PIN = 16
THP_SDL_PIN = 17

BUTTON_PIN = 19

CONFIG_FILE       = 'config.json'
MEASUREMENTS_FILE = 'measure.json'

DEFAULT_CONFIG = {
    "wifi" : [
        {
            "ssid" : "kronos-wifi",
            "key"  : "welcome.to.kronos",
        },
    ],
    "mqtt" : {
        "client_id" : DEVICE_NAME,
        "server"    : "192.168.137.1",
        "port"      : 1883,
        "user"      : "maker",
        "password"  : "this.is.mqtt",
    },
}

DEFAULT_MEASUREMENTS = {
    "data" : [],
}

