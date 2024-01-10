import json
import math

user_position_x = 1
user_position_y = 2

class Mevo:
    def __init__(self):
        mevo_stations_information_filename = 'station_information.json'
        f = open(mevo_stations_information_filename)
        self.stations_information_data = json.load(f)

        mevo_stations_status_filename = 'station_status.json'
        f = open(mevo_stations_status_filename)
        self.stations_status_data = json.load(f)

        mevo_free_bike_filename = 'free_bike_status.json'
        f = open(mevo_free_bike_filename)
        self.free_bike_data = json.load(f)

    def distance_calculate(x1,y1,x2,y2):
        return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

    def are_there_any_bikes(self, entry_count):
        bike_count = self.stations_status_data['data']['stations'][entry_count]['vehicle_types_available'][0]['count']
        bike_count += self.stations_status_data['data']['stations'][entry_count]['vehicle_types_available'][1]['count']
        if bike_count > 0:
            return True
        else:
            return False

    #data/stations/
    def nearest_bike_station(self,user_position_x,user_position_y):

        current_lowest_distance = 1000000000000000000000000000
        current_lowest_distance_station_id = 0
        entry_count = -1
        for entry in self.stations_information_data['data']['stations']:
            entry_count += 1
            station_id = entry['station_id']
            #check if there are any bikes
            if self.are_there_any_bikes(entry_count) == False:
                continue
            stations_x = entry['lat']
            stations_y = entry['lon']
            distance = self.distance_calculate(user_position_x, user_position_y, stations_x, stations_y)
            if distance < current_lowest_distance:
                current_lowest_distance = distance
                current_lowest_distance_station_id = station_id

        print(f"nearest station id: {current_lowest_distance_station_id}, entry: {entry_count}, distance: {current_lowest_distance}")


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


        print(f"nearest ebike: {current_lowest_distance_free_ebike_id}, distance: {current_lowest_distance_ebike}, entry: {current_lowest_distance_ebike_entry}")
        print(f"nearest bike: {current_lowest_distance_free_bike_id}, distance: {current_lowest_distance_bike}, entry: {current_lowest_distance_bike_entry}")
