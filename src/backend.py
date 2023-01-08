from flask import Flask, render_template
import geopandas as gpd
from db import Database
from flask import request
import osmnx  as ox

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


@app.route('/score')
def score():
    lat = request.args.get('lat')
    lon = request.args.get('lng')
    print(lat,lon)

    G = ox.graph_from_place("Venezia, Lido, Venice, Venezia, Veneto, Italy", network_type='all')

    print(G)

    point_nearest_home = ox.distance.nearest_nodes(G,Y=lat,X=long)


    print(point_nearest_home)
    return {'score': lat}


@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(port = 8000, debug = True)