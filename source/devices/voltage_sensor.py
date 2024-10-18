from adafruit_ads1x15.analog_in import AnalogIn

class Voltage_sensor():
    def __init__(self, channel: AnalogIn, r1, r2) -> None:
        self.channel = channel
        self._r1 = r1
        self._r2 = r2

    def get_voltage(self) -> float:
        voltage = self.channel.voltage * (self._r1 + self._r2) / self._r2
        return voltage
