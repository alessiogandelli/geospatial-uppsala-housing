
/* 1 */
// create a basemap
var map = L.map('map').setView([59.8586, 17.6389], 12);


streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);// create an operational layer that is empty for now


let busLayer = L.layerGroup().addTo(map)
let supermarketLayer = L.layerGroup().addTo(map)
let heatmapLayer = L.layerGroup().addTo(map)

university_coords = [59.839815, 17.646617]
//let geocoder = L.Control.geocoder().addTo(map);

// add marker university to map
uni_marker = L.marker(university_coords).addTo(map)





var geocoder = L.Control.geocoder({ defaultMarkGeocode: false, query: 'Uppsala' })
    .on('markgeocode', function (e) {
        coord = e.geocode.center
        console.log(coord)

        var url = `http://127.0.0.1:8000/score?lat=${coord.lat}&lon=${coord.lng}`



        jQuery.getJSON(url, score)


        




    })
    .addTo(map);

/* 2 */
// fill that layer with data from a geojson file
jQuery.getJSON('http://127.0.0.1:8000/stops', function (stops) {

    L.geoJSON(stops, {
        pointToLayer: function (feature, latlng) {
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

jQuery.getJSON('http://127.0.0.1:8000/routes', function (routes) {

    L.geoJSON(routes, { onEachFeature: addBus })
})

// jQuery.getJSON('http://127.0.0.1:8000/heatmap', (data) => {
   
//     // read geojson and add to heatma layer
//     L.geoJSON(data, {
//         style: function(feature) {
//             return {
//                 color: '#ff7800',
//                 weight: 2,
//                 opacity: 1,
//                 fillOpacity: 0.7
//             };
//         }
//     }).addTo(map);




// })




jQuery.getJSON('http://127.0.0.1:8000/supermarkets', function (supermarket) {

    L.geoJSON(supermarket, {
        pointToLayer: function (feature, latlng) {
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






function score(data) {
    console.log(data)
    
    let busClosest = document.getElementById('bus-closest')
    let busLines = document.getElementById('bus-lines')
    let busUni = document.getElementById('bus-uni')
    let walkSupermarket = document.getElementById('walk-supermarket')
    let busHome = document.getElementById('bus-home')


}


/* 4 */
// These options will appear in the control box that users click to show and hide layers
let basemapControl = {
    "My Basemap": streets, // an option to select a basemap (makes more sense if you have multiple basemaps)
}
let layerControl = {
    "Bus": busLayer, // an option to show or hide the layer you created from geojson
    "Supermarket": supermarketLayer,
    "Heatmap": heatmapLayer
}

/* 5 */
// Add the control component, a layer list with checkboxes for operational layers and radio buttons for basemaps
L.control.layers(basemapControl, layerControl).addTo(map)