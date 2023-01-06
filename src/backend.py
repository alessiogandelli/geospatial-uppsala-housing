from flask import Flask, render_template
import geopandas as gpd
from db import Database

app = Flask(__name__)

db = Database()
bus_routes = db.get_bus_routes()
bus_stops = db.get_bus_stops()
markets = db.get_supermarkets()


@app.route('/stops')
def stops():
    return bus_stops.to_json()

@app.route('/routes')
def routes():
    return bus_routes.to_json()

@app.route('/supermarkets')
def supermarkets():
    return markets.to_json()


@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(port = 8000, debug = True)