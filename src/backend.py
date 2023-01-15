from flask import Flask, render_template, request
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from db import Database
import geospatial_utils as geo


from shapely.geometry import Point, Polygon



app = Flask(__name__)

# get data from db
db = Database()
bus_routes = db.get_bus_routes()
bus_stops = db.get_bus_stops()
markets = db.get_supermarkets()
bus_routes = bus_routes.set_index('ref')



# const for city and uni
centrum =  Point([17.6387, 59.8586])
uni = Point([ 17.646617, 59.839815])


#load geo data 
G = geo.load_graph()
bus_stops, bus_routes = geo.get_bus(bus_stops, bus_routes)



# listen for request to the server and send back the data
@app.route('/stops')
def stops():
    
    return bus_stops.to_json()

@app.route('/routes')
def routes():
    print('routes', bus_routes)
    return bus_routes.to_json()

@app.route('/supermarkets')
def supermarkets():
    return markets.to_crs(epsg = 4326).to_json()


@app.route('/score')
def score():
    # get lat and lon from request
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    
    # create point from lat and lon
    home = Point([lon, lat])
    response = geo.get_score(home, bus_stops, markets, centrum, uni, G)

    return response


# def get_distance(start, end):
#     global G
#     G = ox.add_edge_speeds(G)
#     G = ox.add_edge_travel_times(G)

#     #start = gpd.GeoDataFrame({'geometry': start}, index=[0], crs="EPSG:3153").to_crs(epsg=4326).geometry[0]
#     #end = gpd.GeoDataFrame({'geometry': end}, index=[0], crs="EPSG:3152").to_crs(epsg=4326).geometry[0]

#     start_node = ox.distance.nearest_nodes(G, Y=start.y, X=start.x)
#     end_node = ox.distance.nearest_nodes(G, Y=end.y, X=end.x)

#     route = nx.shortest_path(G, start_node, end_node, weight='travel_time')
    
#     edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length')
#     distance = sum(edge_lengths)

#     return distance


# def get_bus_lines(start):
#     # find the closest line from this  bus stop, after a threshold
#     pass





@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(port = 8000, debug=True)