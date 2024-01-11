def algorytm(lista_gitmana):
    from main import mevo
    from main import gmaps
    from main import tier
    lista_do_oddania = []
    start = []
    end_point = []

    print(lista_gitmana)

    if isinstance(lista_gitmana[0], str) == True:
        buffer = gmaps.geocode(lista_gitmana[0])
        start.append((buffer['lat'], buffer['lon']))
    else:
        start.append(lista_gitmana[0])
    if isinstance(lista_gitmana[-1], str) == True:
        buffer = gmaps.geocode(lista_gitmana[-1])
        end_point.append((buffer['lat'], buffer['lon']))
    else:
        end_point.append(lista_gitmana[-1])

    #print(end_point)

    #print(start)
    #mozna zmienic nazwe bo to dlugosc przesiadek
    full_travel_distance = 0
    full_bike_travel_duration = 0
    full_walk_travel_duration = 0
    for i in range(len(lista_gitmana)-1):
        if i == 0:
            continue
        full_bike_travel_duration += gmaps.get_bike_distance(lista_gitmana[i], lista_gitmana[i+1])[0]['duration']
        full_travel_distance += gmaps.get_bike_distance(lista_gitmana[i], lista_gitmana[i+1])[0]['distance']
        full_walk_travel_duration += gmaps.get_walk_distance(lista_gitmana[i], lista_gitmana[i+1])[0]['duration']

    mevo.update_if_needed()


    end_for_mevo = mevo.nearest_bike_station(end_point[0][0], end_point[0][1])
    #zeby ta funkcja odnosila sie do najblizszego przystanku
    #end_for_tier - jakas strefa gdzie mozna zostawic hulajke

    full_walk_travel_duration += gmaps.get_walk_distance(start, lista_gitmana[1])[0]['duration'] #+full_walk_travel_duration

    bikes_dict = mevo.stations_in_radius(start[0][0], start[0][1], 1000)
    bikes_dict.extend(mevo.bikes_in_radius(start[0][0], start[0][1], 1000))
    #print(bikes_dict)
    bikes_list = list()
    fastest_bike = {'id': 0, 'time': 10000000000000, 'lat': 0, 'lon': 0}
    for entry in bikes_dict:
        #print(entry)
        time_value = 0
        buffer = gmaps.get_walk_distance(start[0], [(entry['lat'], entry['lon'])])
        #print(buffer)
        time_value += buffer[0]['duration']
        buffer = gmaps.get_bike_distance([(entry['lat'],entry['lon'])], lista_gitmana[1])
        time_value += buffer[0]['duration']

        #if (entry['range'] != None) and ((entry['range'] * 0.9) < (buffer[0]['distance'] + full_travel_distance)):
            #continue
        time_value += gmaps.get_walk_distance([(end_for_mevo['lat'], end_for_mevo['lon'])], (end_point[0][0], end_point[0][1]))[0]['duration']

        bikes_list.append({'id': entry['id'], 'time': time_value, 'lat': entry['lat'], 'lon': entry['lon']})
        if time_value < fastest_bike['time']:
            fastest_bike['time'] = time_value
            fastest_bike['id'] = entry['id']
            fastest_bike['lat'] = entry['lat']
            fastest_bike['lon'] = entry['lon']
    #print("bike: " + str(fastest_bike))


    tier_dict = tier.get_scooters_data(start[0][0], start[0][1], 500)
    tier_list = list()
    fastest_tier = {'id': 0, 'time': 10000000000000, 'lat': 0, 'lon': 0}
    for entry in tier_dict:
        time_value = 0
        buffer = gmaps.get_walk_distance([start[0]], [(entry['lat'], entry['lon'])])
        time_value += buffer[0]['duration']
        buffer = gmaps.get_bike_distance([(entry['lat'], entry['lon'])], lista_gitmana[1])
        time_value += buffer[0]['duration']

        if (entry['range'] * 0.9) < (buffer[0]['distance'] + full_travel_distance):
            continue

        tier_list.append({'id': entry['id'], 'time': time_value, 'lat': entry['lat'], 'lon': entry['lon']})
        if time_value < fastest_tier['time']:
            fastest_tier['time'] = time_value
            fastest_tier['id'] = entry['id']
            fastest_tier['lat'] = entry['lat']
            fastest_tier['lon'] = entry['lon']
    #print(fastest_tier)

    if fastest_bike['time'] < fastest_tier['time']:

        lista_do_oddania.append({"type": "walk", "path": gmaps.get_walk_direction(start[0], (fastest_bike['lat'], fastest_bike['lon']))})
        for i in range(len(lista_gitmana)-1):
            if i == 0:
                lista_do_oddania.append({"type": "mevo", "path": (gmaps.get_bike_direction((fastest_bike['lat'], fastest_bike['lon']), lista_gitmana[i+1]))})
                continue
            if i == (len(lista_gitmana)-2):
                lista_do_oddania.append({"type": "mevo", "path": gmaps.get_bike_direction(lista_gitmana[i], (end_for_mevo['lat'], end_for_mevo['lon']))})
                lista_do_oddania.append({"type": "walk", "path": gmaps.get_walk_direction((end_for_mevo['lat'], end_for_mevo['lon']), end_point[0])})
                break
            lista_do_oddania.append({"type": "mevo", "path": gmaps.get_bike_direction(lista_gitmana[i], lista_gitmana[i+1])})

    else:
        lista_do_oddania.append({"type": "walk", "path": gmaps.get_walk_direction(start[0], (fastest_tier['lat'], fastest_tier['lon']))})
        for i in range(len(lista_gitmana)-1):
            if i == 0:
                lista_do_oddania.append({"type": "tier", "path": gmaps.get_bike_direction((fastest_tier['lat'], fastest_tier['lon']), lista_gitmana[i+1])})
                continue
            lista_do_oddania.append({"type": "tier", "path": gmaps.get_bike_direction(lista_gitmana[i], lista_gitmana[i+1])})

    return lista_do_oddania

#print(gmaps.get_walk_distance([(user_x, user_y)], bikes_list))
#print(gmaps.get_bike_distance(bikes_list, [(end_x, end_y)]))
