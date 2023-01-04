from flask import Flask
import folium
import pyrosm
import geocoder 
import osmnx as osmnx
import overpass

app = Flask(__name__)

query = '''
(
  node["highway"="bus_stop"](59.781,17.561,59.901,17.717);
  way["highway"="bus_route"](59.781,17.561,59.901,17.717);
  relation["route"="bus"](59.781,17.561,59.901,17.717);
);
'''

@app.route('/')
def index():
    # load  from html to folium
    m = folium.Map(location=[59.8586, 17.6389], zoom_start=12, control_scale=True)
    location = 'uppsala, Ångströmlaboratoriet'
    loc = geocoder.osm(location)
    latlng = [loc.lat, loc.lng]
    m.add_child(folium.Marker(location=latlng, popup=loc.address, icon = folium.Icon(color = 'blue')))


    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)

    api = overpass.API()
    response = api.get(query)



    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)