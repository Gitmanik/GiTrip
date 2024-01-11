
from flask import Flask, render_template, request, jsonify
import api.maps.GoogleMapsProvider
import api.data.TierProvider
import api.data.MevoProvider
import json
import algorithm
import traceback

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
        error_message = f'Error processing request: {str(e)}, {traceback.format_exc()}'
        return jsonify({'error': error_message}), 500

@app.route("/api/allbikes")
def api_allbikes():
    return mevo.get_all_bikes()

@app.route("/api/allbikeparkings")
def api_allbikeparkings():
    return mevo.get_all_bike_parkings()

@app.route("/api/get_path", methods=["POST"])
def api_getpath():
    try:
        data = json.loads(request.data)
        print(data)
        return jsonify(algorithm.algorytm(data)), 200
    except Exception as e:
        error_message = f'Error processing request: {str(e)}, {traceback.format_exc()}'
        print(traceback.format_exc())
        return jsonify({'error': error_message}), 500
