from device import Device
from boot import *
import machine

if __name__ == "__main__":
    machine.freq(WORK_FREQUENCY)
    device = Device()
    device.run()