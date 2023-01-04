#%%
from shapely.wkt import loads
import geopandas as gpd
from db import Database


db = Database()



geometry = loads(route['4'])

# create a geodataframe 
gdf = gpd.GeoDataFrame({'geometry': geometry}, index=[0], crs="EPSG:4326")
# %%

# 
query = "select ref,  ST_AsBinary(way) from planet_osm_line where route = 'bus' "

db = Database()
results = db.query(query)

route = {}

for res in results:
    if res[0] == '4':
        route[res[0]] = wkb.loads(res[1].hex(), hex=True).wkt