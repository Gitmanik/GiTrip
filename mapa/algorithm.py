import json
from main import mevo
from main import gmaps
from main import tier

lista_gitmana = []

start = lista_gitmana[0]

start.append((54.409688, 18.601813))

user_x = start[0][0]
user_y = start[0][1]

route_points = []

route_points.append((54.409688, 18.584187))

end_x = route_points[-1][0]
end_y = route_points[-1][1]

#mozna zmienic nazwe bo to dlugosc przesiadek
full_travel_distance = 0
full_bike_travel_duration = 0
full_walk_travel_duration = 0
for i in range(len(route_points)-1):
    if i == range(len(route_points)-1):
        break
    buffer = gmaps.get_bike_distance(route_points[i], route_points[i+1])
    full_bike_travel_duration += gmaps.get_bike_distance(route_points[i], route_points[i+1])[0]['duration']
    full_travel_distance += gmaps.get_bike_distance(route_points[i], route_points[i+1])[0]['distance']
    full_walk_travel_duration += gmaps.get_walk_distance(route_points[i], route_points[i+1])[0]['duration']

mevo.update_if_needed()

start.append(route_points)
route_points = start

end_for_mevo = mevo.nearest_bike_station(end_x, end_y)
#zeby ta funkcja odnosila sie do najblizszego przystanku
#end_for_tier - jakas strefa gdzie mozna zostawic hulajke

full_walk_travel_duration += gmaps.get_walk_distance(start, route_points[0])[0]['duration'] #+full_walk_travel_duration

bikes_dict = mevo.bikes_in_radius(user_x, user_y, 1000)
bikes_list = list()
fastest_bike = {'id': 0, 'time': 10000000000000, 'lat': 0, 'lon': 0}
for entry in bikes_dict:
    time_value = 0
    buffer = gmaps.get_walk_distance(start, [(entry['lat'],entry['lon'])])
    time_value += buffer[0]['duration']
    buffer = gmaps.get_bike_distance([(entry['lat'],entry['lon'])], route_points[0])
    time_value += buffer[0]['duration']

    if ((entry['range'] * 0.9) < (buffer[0]['distance'] + full_travel_distance)) and (entry['range'] != None):
        continue
    time_value += gmaps.get_walk_distance([(end_for_mevo['lat'],end_for_mevo['lon'])], (end_x, end_y))[0]['duration']

    bikes_list.append({'id': entry['id'], 'time': time_value, 'lat': entry['lat'], 'lon': entry['lon']})
    if time_value < fastest_bike['time']:
        fastest_bike['time'] = time_value
        fastest_bike['id'] = entry['id']
        fastest_bike['lat'] = entry['lat']
        fastest_bike['lon'] = entry['lon']
print(fastest_bike)


tier_dict = tier.get_scooters_data(user_x, user_y, 500)
tier_list = list()
fastest_tier = {'id': 0, 'time': 10000000000000, 'lat': 0, 'lon': 0}
for entry in tier_dict:
    time_value = 0
    buffer = gmaps.get_walk_distance([(user_x, user_y)], [(entry['lat'], entry['lon'])])
    time_value += buffer[0]['duration']
    buffer = gmaps.get_bike_distance([(entry['lat'], entry['lon'])], route_points[0])
    time_value += buffer[0]['duration']

    if (entry['range'] * 0.9) < (buffer[0]['distance'] + full_travel_distance):
        continue

    tier_list.append({'id': entry['id'], 'time': time_value, 'lat': entry['lat'], 'lon': entry['lon']})
    if time_value < fastest_tier['time']:
        fastest_tier['time'] = time_value
        fastest_tier['id'] = entry['id']
        fastest_tier['lat'] = entry['lat']
        fastest_tier['lon'] = entry['lon']
print(fastest_tier)

if fastest_bike['time'] < fastest_tier['time']:


#print(gmaps.get_walk_distance([(user_x, user_y)], bikes_list))
#print(gmaps.get_bike_distance(bikes_list, [(end_x, end_y)]))
