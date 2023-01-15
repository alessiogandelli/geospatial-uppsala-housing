
var map = L.map('map').setView([59.8586, 17.6389], 12);


streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);// create an operational layer that is empty for now


var geocoder = L.Control.geocoder({ defaultMarkGeocode: false, query: 'Uppsala' })
.on('markgeocode', async function (e) {
    coord = e.geocode.center
    console.log(coord)

    let url = `http://127.0.0.1:8000/score?lat=${coord.lat}&lon=${coord.lng}`

    jQuery.getJSON(url, score)

    let score = await fetch(url)


})
.addTo(map);




let busLayer         = L.layerGroup().addTo(map)
let supermarketLayer = L.layerGroup().addTo(map)
let heatmapLayer     = L.layerGroup().addTo(map)

let university_coords = [59.839815, 17.646617]
let uni_marker = L.marker(university_coords).addTo(map)



/* 4 */
// These options will appear in the control box that users click to show and hide layers
let basemapControl = {
  "My Basemap": streets, 
}
let layerControl = {
  "Bus": busLayer, 
  "Supermarket": supermarketLayer,
  "Heatmap": heatmapLayer
}
L.control.layers(basemapControl, layerControl).addTo(map)


async function init () {

    let stops = await fetch('http://127.0.0.1:8000/stops')
    let routes = await fetch('http://127.0.0.1:8000/routes')
    let supermarkets = await fetch('http://127.0.0.1:8000/supermarkets')

    L.geoJSON(routes.json, { onEachFeature: addBus })
    L.geoJSON(stops.json, { onEachFeature: addBus })
    L.geoJSON(supermarkets.json, { onEachFeature: addSupermarket })
    

}






function addBus(feature, layer) {
    
  layer.bindPopup(feature.properties.ref);
  busLayer.addLayer(layer)
  // some other code can go here, like adding a popup with layer.bindPopup("Hello")
}



function addSupermarket(feature, layer) {
  layer.bindPopup(feature.properties.name);
  supermarketLayer.addLayer(layer)
  // some other code can go here, like adding a popup with layer.bindPopup("Hello")
}





init()

