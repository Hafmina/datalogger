import serial
import time
import logging
from collections import namedtuple
from dataclasses import dataclass

@dataclass
class GGA:
    latitude: str
    longitude: str
    altitude: str
    time_utc: time.struct_time
    
@dataclass
class RMC:
    time_utc: time.struct_time
    date: time.struct_time
    latitude: str
    longitude: str
    speed: str

@dataclass
class GPS_data:
    gga_data: GGA
    rmc_data: RMC

class Vk_162:
    def __init__(self, serial_port: serial.Serial) -> None:
        self._serial = serial_port
        self.last_update_timestamp_gga = None
        self.last_update_timestamp_rmc = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.time_utc = None
        self.date = None
        self.speed = None

    def __read_string(self) -> str:
        start_time = time.time()
        
        while self._serial.read().decode() != '$':
            current_time = time.time()
            
            if current_time - start_time > 5:
                return None
            
            pass
        
        return self._serial.readline().decode()
            
    def __decode_gpgga(self, lines) -> GGA:
        
        if lines[6] == "0":
            return None
        
        data_time = time.strptime(lines[1], '%H%M%S.%f')  # UTC time
        data_lat = lines[2][:2].lstrip('0') + "." + "%.7s" % str(float(lines[2][2:]) * 1.0 / 60.0).lstrip("0.") + str(lines[3])
        data_lng = lines[4][:3].lstrip('0') + "." + "%.7s" % str(float(lines[4][3:]) * 1.0 / 60.0).lstrip("0.") + str(lines[5])
        data_alt = "%s%s" % (lines[9], lines[10])
        
        return GGA(data_lat, data_lng, data_alt, data_time)
    
    def __decode_gprmc(self, lines) -> RMC:
        
        if lines[2] != 'A':
            return None
        
        data_time = time.strptime(lines[1], '%H%M%S.%f')  # UTC time
        data_date = time.strptime(lines[9], '%d%m%y')  # UTC date
        data_lat = lines[3][:2].lstrip('0') + "." + "%.7s" % str(float(lines[3][2:]) * 1.0 / 60.0).lstrip("0.") + str(lines[4])
        data_lng = lines[5][:3].lstrip('0') + "." + "%.7s" % str(float(lines[5][3:]) * 1.0 / 60.0).lstrip("0.") + str(lines[6])
        data_spd = lines[7] # In knots
        
        return RMC(data_time, data_date, data_lat, data_lng, data_spd)

    def __is_checksum_valid(self, line: str) -> bool:
        separated_line = line.partition('*')
        checksum = 0
        
        for character in separated_line[0]:
            checksum ^= ord(character)
            
        try:
            input_checksum = int(separated_line[2].rstrip(), 16)
        except:
            print("Error in string")
            return False
        
        if checksum == input_checksum:
            return True
        else:
            print("Invalid checksum")
            return False

    def update_data(self) -> bool:
        """Get GPS longitude, latitude, altitude and time"""
        
        line = self.__read_string()
        if line is None:
            return False
        
        if self.__is_checksum_valid(line) == False:
            return False
        
        gga_data = None
        rmc_data = None
        
        lines = line.split(',')
        if lines[0] == 'GPGGA':
            gga_data = self.__decode_gpgga(lines)
        if lines[0] == 'GPRMC':
            rmc_data = self.__decode_gprmc(lines)
        
        if rmc_data != None:
            self.last_update_timestamp_rmc = time.perf_counter()
            self.time_utc = rmc_data.time_utc
            self.latitude = rmc_data.latitude
            self.longitude = rmc_data.longitude
            self.date = rmc_data.date
            self.speed = rmc_data.speed
        
        if gga_data != None:
            self.last_update_timestamp_gga = time.perf_counter()
            self.latitude = gga_data.latitude
            self.longitude = gga_data.longitude
            self.altitude = gga_data.altitude
            self.time_utc = gga_data.time_utc
            
            return True
        
        return False
    
    def get_latitude(self):
        return self.latitude
    
    def get_longitude(self):
        return self.longitude
    
    def get_altitude(self):
        return self.altitude
    
    def get_time_utc(self):
        return self.time_utc
    
    def get_date(self):
        return self.date
    
    def get_last_update_timestamp_gga(self):
        return self.last_update_timestamp_gga
    
    def get_last_update_timestamp_rmc(self):
        return self.last_update_timestamp_rmc