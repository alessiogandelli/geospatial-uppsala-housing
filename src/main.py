#%%
import geopandas as gpd
import pyrosm
from pyrosm.data import sources
import matplotlib.pyplot as plt
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
import overpy 
import folium
import requests
# %% get data 

'''this give you all the osm data for of all sweden, too big for our purposes'''

# pdb_url = sources.europe.sweden['url']
# pdb_file = requests.get(pdb_url, allow_redirects=True)
# open('sweden.pbf', 'wb').write(pdb_file.content)
# osm_path = "/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/sweden.pbf"

#%%
#uppsala_geojson_path = "/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/uppsalaGeoJSON/df.geojson"

uppsala_osm_path = '/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/uppsala_pbf.osm.pbf'
loc_path = "/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/Tatorter_1980_2018.gpkg"


query = '''

    (
    // query part for: “route=bus” and “ref=4”
    
    node["route"="bus"]["ref"="4"](17.561588703356144, 59.78191521597861, 17.717941431819803, 59.90140795000792);
    way["route"="bus"]["ref"="4"](17.561588703356144, 59.78191521597861, 17.717941431819803, 59.90140795000792);
    relation["route"="bus"]["ref"="4"](17.561588703356144, 59.78191521597861, 17.717941431819803, 59.90140795000792);
    

    );

    out center;

'''

# %% 
'''openstreetmap data'''
osm = pyrosm.OSM(uppsala_osm_path)
buildings = osm.get_buildings()

'''geopackage  data'''
border = gpd.read_file(loc_path)
uppsala_limit = border[border.TATORT == 'Uppsala']
bbox_uppsala = tuple(uppsala_limit.to_crs(epsg=4326).total_bounds)


# %%
# read geopkg


#%%
ax = uppsala_limit.to_crs(epsg=4326).plot(color='white', edgecolor='black')
buildings.plot(ax=ax, color='red')
buildings[buildings['name'] == 'Ångströmlaboratoriet'].plot(ax=ax, color='blue')

webmap = building.explore()

ax.set_ylim(59.83, 59.9)
ax.set_xlim(17.6, 17.7)


# %%
#set figsize 


#osm get public transport


# plot amenities 


#use folium to plot this data 

# create a story about two dragons
story = ''




# %%
geoupp = gpd.read_file(uppsala_geojson_path)


# %%
