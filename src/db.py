#%%
import psycopg2
import dotenv 
import os
from shapely import wkb

dotenv.load_dotenv()


class Database:
    def __init__(self):
        print('connecting to default database ...')
        self._conn = psycopg2.connect(database='geospatial', user='osmone' , password=os.environ['db_pass'], host='localhost')
        self._cursor = self._conn.cursor()

        print('connected to db ' )


    def get_bus_stops(self):
        query = "SELECT name, ST_AsBinary(way) FROM planet_osm_point WHERE highway='bus_stop'"
        self._cursor.execute(query)
        results = self._cursor.fetchall()

        stops = {}

        for result in results:
            stops[result[0]] = wkb.loads(result[1].hex(), hex=True).wkt # translate binary to shapely geometry

        return stops
    
    def get_bus_routes(self):
        query = "select ref,  ST_AsBinary(way) from planet_osm_line where route = 'bus' limit 100"
        self._cursor.execute(query)
        results = self._cursor.fetchall()

        routes = {}

        for result in results:
            print(result)
        


    def query(self, query):
        try:
            print(f'Executing query: {query}')
            self._cursor.execute(query)
            print(f'Fetching results...')
            results = self._cursor.fetchall()
            print(f'Got {len(results)} results')
            return results
        except Exception as e:
            print(f'Error executing query: {e}')
            return None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._conn.close()
    


# %%
