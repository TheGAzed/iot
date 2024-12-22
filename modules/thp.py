from external.bme280_float import BME280

class Thp() :
    result = [0] * 3
    
    def __init__(self, i2c):
        self.sensor = BME280(i2c=i2c)
        
    def measure(self) :
        self.sensor.read_compensated_data(self.result)
    
    @property
    def temperature(self) :
        return self.result[0]
    
    @property
    def humidity(self) :
        return self.result[2]
    
    @property
    def pressure(self) :
        return self.result[1]
        
