from flask import Flask
import folium
import pyrosm

app = Flask(__name__)

@app.route('/')
def index():
    # load  from html to folium
    m = folium.Map(location=[59.8586, 17.6389], zoom_start=12, control_scale=True)


    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)