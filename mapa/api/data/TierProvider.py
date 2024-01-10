import requests


class TierProvider:

    def __init__(self):
        pass

    # radius w metrach?
    def get_scooters_data(self, lat, lng, radius):
        api = {'x-api-key': 'bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2'}
        r = requests.get(f"https://platform.tier-services.io/v1/vehicle?lat={lat}&lng={lng}&radius={radius}", headers = api)

        return r.json()

    