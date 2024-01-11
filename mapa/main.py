
from flask import Flask, render_template, request, jsonify
import api.maps.GoogleMapsProvider
import api.data.TierProvider
import api.data.MevoProvider
import json

gmaps = api.maps.GoogleMapsProvider.GoogleMapsProvider('AIzaSyDsP9RqZORUaJlsX3f1zGJqDJccBNXez4o')

mevo = api.data.MevoProvider.MevoProvider()
tier = api.data.TierProvider.TierProvider()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', gmaps=gmaps.get_map())

@app.route("/api/autocomplete", methods=["POST"])
def api_autocomplete():
    try:
        data = json.loads(request.data)
        input_value = data['input']
        location = (data['lat'], data['lng'])
        return jsonify(gmaps.autocomplete(input_value, location)), 200
    except Exception as e:
        error_message = f'Error processing request: {str(e)}'
        return jsonify({'error': error_message}), 500

@app.route("/api/allbikes")
def api_allbikes():
    return mevo.get_all_bikes()

@app.route("/api/allbikeparkings")
def api_allbikeparkings():
    return mevo.get_all_bike_parkings()

@app.route("/tiertest")
def tier_test():
    return tier.get_scooters_data(54.372158, 18.638306, 1000)

@app.route("/tierzones")
def tier_zones():
    return tier.get_zones()

@app.route("/routetest")
def route_test():
    return gmaps.get_bike_distance(["Gdańsk, Bzowa 1"], ["Gdańsk, Obrońców Wybrzeża 10A", (10, 10)])

@app.route("/test")
def re():
    return gmaps.get_bike_direction("Gdańsk, Bzowa 1", "Gdańsk, Obrońców Wybrzeża 10A")
@app.route("/test2")
def gg():
    return gmaps._get_direc("Gdańsk, Bzowa 1", "Gdańsk, Obrońców Wybrzeża 10A", "bicycling")

@app.route("/mevotest")
def mevo_test():
    mevo.update_if_needed()
    return mevo.nearest_free_bike(54.372158, 18.638306)

@app.route("/places")
def places():
    return gmaps.autocomplete("bzowa 1", (54.354687, 18.593562))