"""Datalogger using a serial GPS module and I2C ADC board to read data from a vehicle.
    Current configured to log DC bus voltage, DC bus current and GPS potition and time
    """

import time
import board
import busio
import serial

from adafruit_ads1x15.analog_in import AnalogIn

from devices.interface.vk_162 import Vk_162
from devices.interface.ads1115 import Ads1115

from devices.current_loop import Current_loop
from devices.voltage_sensor import Voltage_sensor
from devices.gps import Coords

from tasks.csv_save import Save


if __name__ == '__main__':

    # Setup ADC
    i2c_module = busio.I2C(board.SCL, board.SDA)
    ads1115 = Ads1115(i2c_module)

    channel_0: AnalogIn = ads1115.create_channel(0)
    channel_1: AnalogIn = ads1115.create_channel(1)
    channel_2: AnalogIn = ads1115.create_channel(2)

    # Setup GPS
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Open Serial port
    gps = Vk_162(ser)

    # Setup logging
    LOG_NUM = 1
    csv = Save(str(LOG_NUM))
    LOG_NUM = csv.get_log_number() + 1
    csv.save_log_num(LOG_NUM)
    csv = Save(str(LOG_NUM))

    # Setup current and voltage sensor devices
    cur = Current_loop(channel_30a=channel_0, channel_350a=channel_1, g_30a=66.7, g_350a=5.7,
                       offset=-2.45)
    cur.calibrate_offset()
    volt = Voltage_sensor(channel=channel_2, r1=23.55, r2=1.58)

    # Get start time
    start_time = time.monotonic()

    while True:
        time.sleep(1)

        gps.update_data()
        timestamp = time.monotonic()
        voltage = volt.get_voltage()
        current_30a = cur.get_current_30a()
        current_350a = cur.get_current_350a()
        position = Coords(lat=gps.get_latitude(), lng=gps.get_longitude(), alt=gps.get_altitude())

        csv.write_line(time_s=timestamp, volt=voltage, amps_30=current_30a, amps_350=current_350a,
                       position=position)

        # Create new file after 24h = 24 * 60 * 60 seconds
        if (timestamp - start_time) > (12 * 60 * 60):
            LOG_NUM += 1
            start_time = timestamp
            csv = Save(str(LOG_NUM))
            csv.save_log_num(LOG_NUM)
