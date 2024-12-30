class Photo() :
    def __init__(self, adr) :
        self.sensor = adr
        
    def measure(self) :
        #self.luminosity = self.sensor.read_u16()
        self.luminosity = round((self.sensor.read_u16() / 65536) * 100, 3)
