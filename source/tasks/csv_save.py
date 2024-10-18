import csv
from devices.gps import Coords

class Save:
    def __init__(self, log_num: str) -> None:
        self.logname: str = "./logs_are_here/log_%s.csv" % log_num
        with open(self.logname, 'w', newline='') as _csv_file:
            writer = csv.writer(_csv_file)
            writer.writerow(["Time [s]", "Voltage [V]", "Current 30A [A]", "Current 350A [A]", "Latitude [rad]", "Longitude [rad]", "Altitude [m]"])
    
    def write_line(self, time_s: int, volt: float, amps_30: float, amps_350: float, position: Coords):
        
        data = [str(time_s), str(volt), str(amps_30), str(amps_350), position.lat, position.lng, position.alt]
        
        with open(self.logname, 'a', newline='') as _csv_file:
            writer = csv.writer(_csv_file)
            writer.writerow(data)
            
    
    def save_log_num(self, log_num: int) -> None:
        filename = "./logs_are_here/current_log_number.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(log_num)])
            
    def get_log_number(self) -> int:
        filename = "./logs_are_here/current_log_number.csv"
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                return int(row[0])
