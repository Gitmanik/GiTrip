import math
import requests
import time


class MevoProvider:

    def __init__(self):
        self.last_updated = 0
        self.free_bike_data = None
        self.stations_status_data = None
        self.stations_information_data = None

    def update_if_needed(self):
        if time.time() - self.last_updated > 30:
            self.update_data()

    def update_data(self):
        self.stations_information_data = self.get_json_data('station_information')
        self.stations_status_data = self.get_json_data('station_status')
        self.free_bike_data = self.get_json_data('free_bike_status')
        self.last_updated = time.time()

    def get_json_data(self, json_name):
        api = {'Client-Identifier': 'gitcorp-hackathon2024'}
        r = requests.get(f"https://gbfs.urbansharing.com/rowermevo.pl/{json_name}.json", headers=api)
        return r.json()

    def distance_calculate(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    def are_there_any_bikes(self, entry_count):
        self.update_if_needed()
        bike_count = self.stations_status_data['data']['stations'][entry_count]['vehicle_types_available'][0]['count']
        bike_count += self.stations_status_data['data']['stations'][entry_count]['vehicle_types_available'][1]['count']
        if bike_count > 0:
            return True
        else:
            return False

    # data/stations/
    def nearest_bike_station(self, user_position_x, user_position_y):
        current_lowest_distance = 1000000000000000000000000000
        current_lowest_distance_station_id = 0
        entry_count = -1
        for entry in self.stations_information_data['data']['stations']:
            entry_count += 1
            station_id = entry['station_id']
            # check if there are any bikes
            if self.are_there_any_bikes(entry_count) == False:
                continue

            stations_x = entry['lat']
            stations_y = entry['lon']
            # TODO: TUTAJ GOOGLE MAPS DISTANCE MATRIX
            distance = self.distance_calculate(user_position_x, user_position_y, stations_x, stations_y)
            if distance < current_lowest_distance:
                current_lowest_distance = distance
                current_lowest_distance_station_id = station_id

        return {"id": current_lowest_distance_station_id, "entry": entry_count, "distance": current_lowest_distance }

    def nearest_free_bike(self, user_position_x, user_position_y):
        current_lowest_distance_ebike = 1000000000000000000000000000
        current_lowest_distance_bike = 1000000000000000000000000000
        current_lowest_distance_free_bike_id = 0
        current_lowest_distance_free_ebike_id = 0
        current_lowest_distance_ebike_entry = 0
        current_lowest_distance_bike_entry = 0
        entry_count = -1
        for entry in self.free_bike_data['data']['bikes']:
            entry_count += 1
            free_bike_id = entry['bike_id']
            free_bike_x = entry['lat']
            free_bike_y = entry['lon']
            # TODO: TUTAJ GOOGLE MAPS DISTANCE MATRIX
            distance = self.distance_calculate(user_position_x, user_position_y, free_bike_x, free_bike_y)
            if entry['vehicle_type_id'] == 'ebike':
                if distance < current_lowest_distance_ebike:
                    current_lowest_distance_ebike = distance
                    current_lowest_distance_free_ebike_id = free_bike_id
                    current_lowest_distance_ebike_entry = entry_count
            else:
                if distance < current_lowest_distance_bike:
                    current_lowest_distance_bike = distance
                    current_lowest_distance_free_bike_id = free_bike_id
                    current_lowest_distance_bike_entry = entry_count

        return {
            "nearest_bike": {
                "id": current_lowest_distance_free_bike_id,
                "distance": current_lowest_distance_bike,
                "entry": current_lowest_distance_bike_entry},
            "nearest_ebike": {
                "id": current_lowest_distance_free_ebike_id,
                "distance": current_lowest_distance_ebike,
                "entry": current_lowest_distance_ebike_entry}
            }

    def get_all_bikes(self):

        self.update_if_needed()
        to_ret = list()

        for entry in self.stations_information_data['data']['stations']:
            to_ret.append

        for entry in self.free_bike_data['data']['bikes']:


            to_ret.append( {
                "bike_id": entry['bike_id'],
                "type": entry['vehicle_type_id'],
            "lat": entry['lat'],
            "lon": entry['lon']
            })

        return to_ret

    def bikes_in_radius(self, x, y, radius):
        dictionary = {}
        bikes_in_radius_count = 0
        for entry in self.free_bike_data['data']['bikes']:
            free_bike_x = entry['lat']
            free_bike_y = entry['lon']
            distance = self.distance_calculate(x, y, free_bike_x, free_bike_y)
            if distance <= radius:
                dictionary[bikes_in_radius_count] = {
                    'lat': entry['lat'],
                    'lon': entry['lon'],
                    'vehicle': entry['vehicle_type_id'],
                    'range': entry['current_range_meters']
                }
                bikes_in_radius_count += 1
        return dictionary

    def stations_in_radius(self, x, y, radius):
        dictionary = {}
        stations_in_radius_count = 0
        entry_count = -1
        for entry in self.stations_information_data['data']['stations']:
            entry_count += 1
            stations_x = entry['lat']
            stations_y = entry['lon']
            distance = self.distance_calculate(x, y, stations_x, stations_y)
            if distance <= radius:
                dictionary[stations_in_radius_count] = {
                    'lat': entry['lat'],
                    'lon': entry['lon'],
                    'bike_count': self.stations_status_data['data']['stations'][entry_count]['vehicle_types_available'][0]['count'],
                    'ebike_count': self.stations_status_data['data']['stations'][entry_count]['vehicle_types_available'][1]['count']
                }
                stations_in_radius_count += 1
        return dictionary


