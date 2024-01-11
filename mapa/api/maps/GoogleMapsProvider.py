import googlemaps


class GoogleMapsProvider:

    def __init__(self, apikey):
        self.client = googlemaps.Client(key=apikey)
        self.apikey = apikey

    def get_map(self):
        return f'''
<script>
    (g=>{{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={{}});var d=b.maps||(b.maps={{}}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${{c}}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))}})({{
    key: "{self.apikey}",
    v: "weekly",
}});
</script>
'''

    def get_bike_distance(self, start, target):
        return self._get_distance_common(start, target, "bicycling")
    def get_walk_distance(self, start, target):
        return self._get_distance_common(start, target, "walking")

    def _get_distance_common(self, start, target, type):
        resp = self.client.distance_matrix(start, target, mode=type, language="pl-PL")

        resp = resp['rows'][0]['elements']

        to_ret = list()
        for row in resp:
            to_ret.append({"distance": row['distance']['value'],
                            "duration": resp['duration']['value']})

        return to_ret

    def get_bike_direction(self, start, target):
        return self._get_directions_common(start, target, "bicycling")
    def get_walk_direction(self, start, target):
        return self._get_directions_common(start, target, "walking")

    def _get_directions_common(self, start, target, type):
        resp = self.client.directions(start, target, mode=type, language="pl-PL")

        resp = resp[0]

        return {"distance": resp['legs'][0]['distance']['value'],
                "duration": resp['legs'][0]['duration']['value'],
                "polyline": resp['overview_polyline']['points']}

    def autocomplete(self, input, location):
        data = self.client.places_autocomplete(input, location = location, radius = 50, language = 'pl-PL')

        try:
            to_ret = list()

            max_ctr = 5
            ctr = 0
            for place in data:
                if ctr > max_ctr:
                    break
                details = self.client.place(place['place_id'], fields=['formatted_address'], language='pl-PL')

                to_ret.append((place['description'], details['result']['formatted_address']))
                ctr += 1

            return to_ret

        except Exception as e:
            print(e)
            return None

        return to_ret