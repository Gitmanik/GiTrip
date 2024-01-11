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


    def distance_calculate(self, lat1, lon1, lat2, lon2):
        R = 6371  # promień Ziemi w kilometrach

        # konwersja stopni na radiany
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # różnice szerokości i długości geograficznych
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # obliczenie wzoru haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        distance *= 1000

        return distance

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
        best_station_x = 0
        best_station_y = 0
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
                best_station_x = stations_x
                best_station_y = stations_y

        #return {"id": current_lowest_distance_station_id, "entry": entry_count, "distance": current_lowest_distance }
        return {'lat': best_station_x, 'lon': best_station_y}

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

        #for entry in self.stations_information_data['data']['stations']:
            #to_ret.append

        for entry in self.free_bike_data['data']['bikes']:


            to_ret.append( {
                "bike_id": entry['bike_id'],
                "type": entry['vehicle_type_id'],
                "lat": entry['lat'],
                "lng": entry['lon']
            })

        return to_ret

    def bikes_in_radius(self, x, y, radius):
        dictionary = list()
        bikes_in_radius_count = 0
        for entry in self.free_bike_data['data']['bikes']:
            free_bike_x = entry['lat']
            free_bike_y = entry['lon']
            distance = self.distance_calculate(x, y, free_bike_x, free_bike_y)
            if distance <= radius:
                dictionary.append({
                    'lat': entry['lat'],
                    'lon': entry['lon'],
                    'vehicle': entry['vehicle_type_id'],
                    'range': entry['current_range_meters'],
                    'id': entry['bike_id']
                })
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


