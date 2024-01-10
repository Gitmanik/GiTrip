
from flask import Flask, render_template, request, jsonify
import api.maps.GoogleMapsProvider
import api.data.TierProvider

gmaps = api.maps.GoogleMapsProvider.GoogleMapsProvider('AIzaSyDsP9RqZORUaJlsX3f1zGJqDJccBNXez4o')

tier = api.data.TierProvider.TierProvider()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', gmaps=gmaps.get_map())

@app.route("/nasze-api", methods=["POST"])
def nasze_api():
    try:
        input_value = request.form.get('input')
        # Do something with the input_value, for example, process it and return a response
        response_data = {'message': 'Request received successfully', 'input': input_value}
        return jsonify(response_data), 200
    except Exception as e:
        error_message = f'Error processing request: {str(e)}'
        return jsonify({'error': error_message}), 500

@app.route("/tiertest")
def tier_test():
    return tier.get_scooters_data(54.372158, 18.638306, 1000)