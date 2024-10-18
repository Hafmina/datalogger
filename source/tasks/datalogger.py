from statemachine import State, StateMachine
import time

from devices.current_loop import Current_loop
from devices.voltage_sensor import Voltage_sensor

# Generate diagram: python -m statemachine.contrib.diagram tasks.datalogger.Datalogger ../m.png

class Datalogger(StateMachine):

    startup = State(initial=True)
    finding_date = State()
    logging = State("logging")
    idle = State()

    read_timestamp = startup.to(finding_date, cond="startup_time_elapsed")
    read_gps_signal = finding_date.to(idle, cond="gps_signal_found")
    check_movement = idle.to(logging, cond="has_started_moving")
    log_adc = logging.to(logging)
    log_gps = logging.to(logging)
    check_movement = logging.to(idle, cond="has_stopped_moving")
    create_new_csv = logging.to(finding_date, cond="is_new_day")

    def __init__(self, current_loop_instance: Current_loop, voltage_sensor_instance: Voltage_sensor):
        self.startup_timestamp = None
        self.current_loop = current_loop_instance
        self.voltage_sensor = voltage_sensor_instance
        super().__init__()

    def before_startup(self):
        self.startup_timestamp = time.time()

    def startup_time_elapsed(self) -> bool:
        time_to_elapse_s = 5  # TODO: Set to an appropriate value
        current_timestamp = time.time()

        return current_timestamp - self.startup_timestamp >= time_to_elapse_s

    def before_logging(self):
        current_30a = self.current_loop.get_current_30a()
        current_300a = self.current_loop.get_current_300a()
        voltage = self.voltage_sensor.get_voltage()
    
    
# import subprocess
# from datetime import datetime

# def set_system_time(gps_date, gps_time):
#     # Format the date and time from GPS
#     datetime_string = f"{gps_date.strftime('%Y-%m-%d')} {gps_time.strftime('%H:%M:%S')}"
    
#     # Use subprocess to run the 'date' command to set the system time
#     subprocess.run(['sudo', 'date', '--set', datetime_string])

# # Example usage:
# set_system_time(gps_date, gps_time)
