#%%
from shapely.wkt import loads
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from db import Database
import folium
import geocoder
from shapely.wkt import loads
from shapely import wkb

import folium
from folium import Map
from folium.map import Layer, FeatureGroup,LayerControl,Marker
from folium.plugins import MarkerCluster, FeatureGroupSubGroup, Fullscreen, HeatMap


db = Database()
routes = db.get_bus_routes()
stops = db.get_bus_stops()
supermarkets = db.get_supermarkets()


save_path = '/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/uppsalaGeoJSON/'
routes.to_file(save_path + 'routes.geojson', driver='GeoJSON')
stops.to_file(save_path + 'stops.geojson', driver='GeoJSON')
supermarkets.to_file(save_path + 'supermarkets.geojson', driver='GeoJSON')



#%%
'''BUS ROUTES'''

m = folium.Map(location=[59.8586, 17.6389], zoom_start=12, control_scale=True)
location = 'uppsala, Ångströmlaboratoriet'
loc = geocoder.osm(location)
latlng = [loc.lat, loc.lng]

# add lab 
m.add_child(folium.Marker(location=latlng, popup=loc.address, icon = folium.Icon(color = 'blue')))



'''intercative bus routes'''
feature_groups = {}
for ref in routes['ref'].unique():
    feature_groups[ref] = folium.FeatureGroup(name=str(ref), show=False)

# Add the routes to the appropriate FeatureGroup
for _, row in routes.iterrows():
    ref = row['ref']
    geometry = row['geometry']
    folium.GeoJson(geometry, name=str(ref)).add_to(feature_groups[ref])

# Add the FeatureGroups to the map
for _, feature_group in feature_groups.items():
    feature_group.add_to(m)

# Add a layer control widget to the map
folium.LayerControl().add_to(m)

'''bus stops'''
#display bus stop from geodataframe
for _, row in stops.iterrows():
    latlng = [row['geometry'].y, row['geometry'].x]
    m.add_child(folium.Circle(location=latlng, popup=row['name'], radius = 1, color = 'green', fill = True, fill_color = 'red'))



# con you add a button to hide all routes 
# https://stackoverflow.com/questions/51034863/how-to-hide-all-layers-in-folium-map

m



#%%




# heatmap with supermarket distance 
#HeatMap(supermarkets[['lat', 'lon']].values.tolist(), radius=50).add_to(m)

# toggle button to show/hide heatmap 





m


# %%
''' map with bus routes and stops '''


m = folium.Map(location=[59.8586, 17.6389], zoom_start=12, control_scale=True)

markers_group = FeatureGroup(name='Lab', show=False)
bus_group = FeatureGroup(name='bus', show=False)
heat_group = FeatureGroup(name='heat', show=False)
supermarkets_group = FeatureGroup(name='supermarkets', show=False)


'''LAB LOCATION'''
location = 'uppsala, Ångströmlaboratoriet'
loc = geocoder.osm(location)
latlng = [loc.lat, loc.lng]

folium.Marker(location=latlng, popup=loc.address, icon = folium.Icon(color = 'blue')).add_to(markers_group)
home = folium.Marker(location=[59.8586, 17.6389], popup='home', draggable = True ,icon = folium.Icon(icon = 'home')).add_to(m)




'''BUS ROUTES'''
for route in routes['ref'].unique():
    bus_group.add_child(folium.GeoJson( routes[routes['ref'] == route]['geometry'].values[0], 
                                        name=str(route))) 

for _, row in stops.iterrows():
    latlng = [row['geometry'].y, row['geometry'].x]
    bus_group.add_child(folium.Circle(  location=latlng, popup=row['name'], radius = 1, 
                                        color = 'green', fill = True, fill_color = 'red'))


'''SUPERMARKETS'''

#display supermarkets from geodataframe
for _, row in supermarkets.iterrows():
    latlng = [row['geometry'].y, row['geometry'].x]
    supermarkets_group.add_child(folium.Circle(location=latlng, popup=row['name'], radius = 1, color = 'red', fill = True, fill_color = 'green'))



marker_cluster = ClickForMarker()
marker_cluster.add_to(m)


bus_group.add_to(m)
markers_group.add_to(m)
heat_group.add_to(m)
supermarkets_group.add_to(m)

folium.LayerControl().add_to(m)

m# %%

# compute distance from marker home to closest supermarket

from shapely.geometry import Point
from shapely.ops import nearest_points

# create a point from home location
home = Point([59.8586, 17.6389])

# find the nearest supermarket
nearest = nearest_points(home, supermarkets['geometry'].values[0])
nearest[0].distance(nearest[1])




# %%

# %%


# %%


import datetime
# %%
import osmnx  as ox
G = ox.graph_from_point( center_point=(59.8586, 17.6389), dist=8000, network_type='walk')

G = ox.speed.add_edge_speeds(G)
G = ox.speed.add_edge_travel_times(G)

#
orig = ox.distance.nearest_nodes(G, Y=59.8586, X=17.6389)
dest = ox.distance.nearest_nodes(G, Y=59.839815, X=17.646617)

route = ox.shortest_path(G, orig, dest, weight="travel_time")

travel_speed = 5 
trip_times = [5, 10, 15, 20, 25] 

edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
print( 'length:', round(sum(edge_lengths)))

edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "travel_time")
print(str(datetime.timedelta(seconds=sum(edge_lengths))))

# %%
iso_colors = ox.plot.get_colors(n=len(trip_times), cmap="plasma", start=0, return_hex=True)


# color the nodes according to isochrone then plot the street network

# %%