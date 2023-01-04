#%%
import psycopg2
import dotenv 
import os
from shapely import wkb
dotenv.load_dotenv()

# Connect to the database
conn = psycopg2.connect(database='geospatial', user='osmone' , password=os.environ['db_pass'], host='localhost')

# Create a cursor
cur = conn.cursor()

# Execute a SQL query to retrieve the OSM data
query = "SELECT name, ST_AsBinary(way) FROM planet_osm_point"
cur.execute(query)

# Fetch the results of the query
results = cur.fetchall()

# Print the results
for result in results:
    point = wkb.loads(result[1].hex(), hex=True)
    print(result[0], point)

# Close the cursor and connection
cur.close()
conn.close()
# %%

class Database:
    def __init__(self):
        print('connecting to default database ...')
        self._conn = psycopg2.connect(database='geospatial', user='osmone' , password=os.environ['db_pass'], host='localhost')
        self._cursor = self._conn.cursor()

        print('connected to db ' )


    def get_bus_stops(self):
        query = "SELECT name, ST_AsBinary(way) FROM planet_osm_point"
        self._cursor.execute(query)
        results = self._cursor.fetchall()

        stops = {}

        for result in results:
            stops[result[0]] = wkb.loads(result[1].hex(), hex=True).wkt # translate binary to shapely geometry

        return stops


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._conn.close()
    


# %%
