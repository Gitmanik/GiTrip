from flask import Flask, render_template
import api.maps.GoogleMapsProvider

gmaps = api.maps.GoogleMapsProvider.GoogleMapsProvider('AIzaSyDsP9RqZORUaJlsX3f1zGJqDJccBNXez4o')

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', gmaps=gmaps.get_map())
