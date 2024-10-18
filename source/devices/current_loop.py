from adafruit_ads1x15.analog_in import AnalogIn

class Current_loop():
    def __init__(self, channel_30a: AnalogIn, channel_350a: AnalogIn, g_30a: float, g_350a: float, offset: float) -> None:
        self._channel_30a = channel_30a
        self._channel_350a = channel_350a
        self._g_30a = g_30a
        self._g_350a = g_350a
        self._offset = offset

    def get_current_30a(self) -> float:
        voltage = self._channel_30a.voltage
        current = (voltage + self._offset) * (1/self._g_30a) * 1000
        return current

    def get_current_350a(self) -> float:
        voltage = self._channel_350a.voltage
        current = (voltage + self._offset) * (1/self._g_350a) * 1000
        return current

    def calibrate_offset(self) -> None:
        self._offset = -self._channel_350a.voltage