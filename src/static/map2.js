
/* 1 */
// create a basemap
var map = L.map('map').setView([59.8586, 17.6389], 12);


streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);// create an operational layer that is empty for now


let busLayer = L.layerGroup().addTo( map )
let supermarketLayer = L.layerGroup().addTo( map )

/* 2 */
// fill that layer with data from a geojson file
jQuery.getJSON( 'http://127.0.0.1:8000/stops', function(stops){

    L.geoJSON(stops, {
        pointToLayer: function(feature, latlng) {
            return L.circle(latlng, {
                radius: 5,  // radius in meters
                color: 'green',
                fillColor: '#f03',
                fillOpacity: 0.5
            });
            },
        onEachFeature: addBus
    })
})

jQuery.getJSON( 'http://127.0.0.1:8000/routes', function(routes){

    L.geoJSON(routes, {onEachFeature: addBus})
})


jQuery.getJSON( 'http://127.0.0.1:8000/supermarkets', function(supermarket){

    L.geoJSON(supermarket, {
        pointToLayer: function(feature, latlng) {
            return L.circle(latlng, {
                radius: 10,  // radius in meters
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.5
            });
            },
        onEachFeature: addSupermarket
    })
})





/* 3 */
// This function is run for every feature found in the geojson file. It adds the feature to the empty layer we created above
function addBus( feature, layer ){
  layer.bindPopup(feature.properties.name);
  busLayer.addLayer( layer )
  // some other code can go here, like adding a popup with layer.bindPopup("Hello")
}

function addSupermarket( feature, layer ){
    layer.bindPopup(feature.properties.name);
    supermarketLayer.addLayer( layer )
    // some other code can go here, like adding a popup with layer.bindPopup("Hello")
  }






/* 4 */
// These options will appear in the control box that users click to show and hide layers
let basemapControl = {
  "My Basemap": streets, // an option to select a basemap (makes more sense if you have multiple basemaps)
}
let layerControl = {
  "Bus": busLayer, // an option to show or hide the layer you created from geojson
  "Supermarket": supermarketLayer
}

/* 5 */
// Add the control component, a layer list with checkboxes for operational layers and radio buttons for basemaps
L.control.layers( basemapControl, layerControl ).addTo( map )