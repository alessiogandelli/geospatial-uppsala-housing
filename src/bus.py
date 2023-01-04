#%%
from shapely.wkt import loads
import geopandas as gpd
from db import Database


db = Database()
routes = db.get_bus_routes()
stops = db.get_bus_stops()


#%%


# %%
