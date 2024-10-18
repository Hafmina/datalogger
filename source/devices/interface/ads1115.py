import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class Ads1115:
    def __init__(self, i2c) -> None:
        self.i2c = i2c
        self.ads = ADS.ADS1115(self.i2c)
        
    def create_channel(self, channel_number: int) -> AnalogIn:
        return AnalogIn(self.ads, channel_number)