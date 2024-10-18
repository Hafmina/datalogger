import numpy as np

from devices.interface.vk_162 import Vk_162

class Coords:
    def __init__(self, lat: str, lng: str, alt: str = "XXX") -> None:
        self.lat = lat
        self.lng = lng
        self.alt = alt
        
    def parse(self) -> tuple[float, float]:

        if (self.lat or self.lng) == None:
            return None, None

        deg_lat = int(self.lat[:2])
        min_lat = float(self.lat[2:-1])
        lat_decimal = np.deg2rad(deg_lat + min_lat / 60)

        deg_lng = int(self.lng[:2])
        min_lng = float(self.lng[2:-1])
        lng_decimal = np.deg2rad(deg_lng + min_lng / 60)

        return lat_decimal, lng_decimal

class Gps:
    def __init__(self, vk_162: Vk_162) -> None:
        self.vk_162 = vk_162
    
    def get_distance(self, start: Coords, end: Coords) -> float:
        # phi = lat
        # lambda = lng
        R = 6371e3
        delta_lambda = end.lng - start.lng
        delta_phi = end.lat - start.lat
        B_x = np.cos(end.lat) * np.cos(delta_lambda)
        B_y = np.cos(end.lat) * np.sin(delta_lambda)
        A_1 = np.sin(start.lat) + np.sin(end.lat)
        A_2 = np.sqrt(np.pow((np.cos(start.lat) + B_x), 2) + np.pow(B_y, 2))
        phi_m = np.atan2(A_1, A_2)
        
        x = delta_lambda * np.cos(phi_m)
        y = delta_phi
        d = R * np.sqrt(np.pow(x, 2), np.pow(y, 2))

    def get_position(self) -> Coords:
        self.vk_162.update_data()
        lat = self.vk_162.latitude
        lng = self.vk_162.longitude
        return Coords(lat=lat, lng=lng)