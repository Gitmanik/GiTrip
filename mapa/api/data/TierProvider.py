import requests


class TierProvider:

    def __init__(self):
        self.apikey = {'x-api-key': 'bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2'}
        pass

    # radius w metrach?
    def get_scooters_data(self, lat, lng, radius):
        r = requests.get(f"https://platform.tier-services.io/v1/vehicle?lat={lat}&lng={lng}&radius={radius}", headers = self.apikey)

        all_scooters = r.json()
        all_scooters = all_scooters['data']

        #print(all_scooters)

        to_ret = list()

        for scooter in all_scooters:
            #print(scooter)
            #if not scooter['is_rentable']:
            #    continue
            to_ret.append({
                'id': scooter['id'],
                'max_speed': scooter['attributes']['maxSpeed'],
                'lat': scooter['attributes']['lat'],
                'lon': scooter['attributes']['lng'],
                'range': scooter['attributes']['currentRangeMeters']
            })

        return to_ret

    def get_zones(self):
        r = requests.get(f"https://platform.tier-services.io/v1/zone/GDANSK/subzone", headers = self.apikey)

        all_zones = r.json()
        return all_zones
    