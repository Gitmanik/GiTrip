from flask import Flask, render_template
import api.maps.GoogleMapsProvider
import api.data.TierProvider

gmaps = api.maps.GoogleMapsProvider.GoogleMapsProvider('AIzaSyDsP9RqZORUaJlsX3f1zGJqDJccBNXez4o')

tier = api.data.TierProvider.TierProvider()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', gmaps=gmaps.get_map())

@app.route("/tiertest")
def tier_test():
    return tier.get_scooters_data(54.372158, 18.638306, 1000)