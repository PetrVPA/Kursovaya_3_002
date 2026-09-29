from abc import ABC, abstractmethod
from requests import get


class CoordinatesObject(ABC):
    @abstractmethod
    def get_coordinates(self):
        pass


class APIAirplane(CoordinatesObject):

    def __init__(self):
        self.opensky_url = 'https://opensky-network.org/api/states/all?'
        self.aeroplanes = None

    def get_coordinates(self, params: dict):
        response = get(url=self.opensky_url, params=params)
        self.aeroplanes = response.json()
        return self.aeroplanes


class APIState(CoordinatesObject):

    def __init__(self):
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.params = {}

    def get_coordinates(self, country: str) -> dict:
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
        data = response.json()
        #print(data)
        geo_coordinates = data[0].get('boundingbox')
        params = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }
        return params


class Airplane():
    calsing: str
    state: str
    baro_altitude: float
    velocity: float
    true_track: float

    def __init__(self, calsing, state, baro_altitude, velocity, true_track):
        self.__calsing = calsing
        self.__state = state
        self.__baro_altitude = baro_altitude
        self.__velocity = velocity
        self.__true_track = true_track

    def add_airplane(self, params):
        self.calsing = params[1]
        self.state = params[2]
        self.baro_altitude = params[7]
        self.velocity = params[9]
        self.true_track = params[10]

    @property
    def calsing(self):
        return self.__calsing

    @calsing.setter
    def calsing(self, value):
        if value(type) == str:
            self.__calsing = value
            return self.__calsing

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if value(type) == str:
            self.__state = value

    @property
    def baro_altitude(self):
        return self.__baro_altitude

    @baro_altitude.setter
    def baro_altitude(self, value):
        if value >= 0 and value <= 35000.0:
            self.__baro_altitude = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        if value >= 0 and value <= 330.0:
            self.__velocity = value

    @property
    def true_track(self):
        return self.__true_track

    @true_track.setter
    def true_track(self, value):
        if (value >= 0.0) and (value <= 360.0):
            self.__true_track = value

    def altitude_more(self, other):
        if other.baro_altitude < self.baro_altitude:
            return True
        else:
            return False

    def velocity_more(self, other):
        if other.velocity < self.velocity:
            return True
        else:
            return False

    def __str__(self):
        return (f'Борт: {self.calsing}, {self.state}, {self.baro_altitude} м, '
                f'{self.velocity} м/сек, курс: {self.true_track}')

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'calsing': self.calsing,
            'state': self.state,
            'baro_altitude': self.baro_altitude,
            'velocity': self.velocity,
            'true_track': self.true_track
        }
