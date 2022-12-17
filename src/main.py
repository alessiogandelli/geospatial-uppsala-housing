#%%
import geopandas as gpd
import pyrosm
from pyrosm.data import sources
import matplotlib.pyplot as plt
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

import requests
# %% get data 
pdb_url = sources.europe.sweden['url']
pdb_file = requests.get(pdb_url, allow_redirects=True)
open('sweden.pbf', 'wb').write(pdb_file.content)

#%%
loc_path = "/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/Tatorter_1980_2018.gpkg"
osm_path = "/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/sweden.pbf"
uppsala_geojson_path = "/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/uppsalaGeoJSON/df.geojson"
uppsala_osm_path = '/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/uppsala_pbf.osm.pbf'
# filter pdb on coorindates 


# %% open street map data 
osm = pyrosm.OSM(uppsala_osm_path)
osm.get_buildings().plot()
plt.show()

# %%
# read geopkg
loc = gpd.read_file(loc_path)
uppsala_limit = loc[loc.TATORT == 'Uppsala']


ax = uppsala_limit.to_crs(epsg=4326).plot(color='white', edgecolor='black')
buildings = osm.get_buildings()
buildings.plot(ax=ax, color='red')
buildings[buildings['name'] == 'Ångströmlaboratoriet'].plot(ax=ax, color='blue')
# plot amenities 







# %%
geoupp = gpd.read_file(uppsala_geojson_path)


# %%
