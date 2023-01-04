#%%
from shapely.wkt import loads
import geopandas as gpd
from db import Database
import folium
import geocoder


db = Database()
routes = db.get_bus_routes()
stops = db.get_bus_stops()


#%%
m = folium.Map(location=[59.8586, 17.6389], zoom_start=12, control_scale=True)
location = 'uppsala, Ångströmlaboratoriet'
loc = geocoder.osm(location)
latlng = [loc.lat, loc.lng]
m.add_child(folium.Marker(location=latlng, popup=loc.address, icon = folium.Icon(color = 'blue')))





feature_groups = {}
for ref in routes['ref'].unique():
    feature_groups[ref] = folium.FeatureGroup(name=str(ref))

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

m

# %%
feature_groups = {}
for ref in routes['ref'].unique():
    feature_groups[ref] = folium.FeatureGroup(name=str(ref))

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

m
# %%
