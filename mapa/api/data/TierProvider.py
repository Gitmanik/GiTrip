import requests


class TierProvider:

    def __init__(self):
        pass

    # radius w metrach?
    def get_scooters_data(self, lat, lng, radius):
        api = {'x-api-key': 'bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2'}
        r = requests.get(f"https://platform.tier-services.io/v1/vehicle?lat={lat}&lng={lng}&radius={radius}", headers = api)

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

    