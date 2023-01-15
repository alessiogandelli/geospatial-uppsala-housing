

let time_uni = 0
let time_center = 0
let time_supermarket = 0
let data = {}

let bikeUni = document.getElementById('bike-uni')
let bikeCenter = document.getElementById('bike-center')
let bikeSupermarket = document.getElementById('bike-supermarket')

function showValue(value) {
    
    document.getElementById("slider-value").innerHTML = value;

    time_uni =  ((data.home_uni/1000)/ value) * 60
    time_center = ((data.home_center/1000)/ value) * 60
    time_supermarket = ((data.home_supermarket/1000)/ value) * 60

    console.log(time_uni)

    bikeUni.innerHTML = 'time from home to university: ' + Math.round(time_uni)+ 'min'
    bikeCenter.innerHTML = 'time from home to city center: ' + Math.round(time_center) + 'min'
    bikeSupermarket.innerHTML = 'time from home to supermarket: ' + Math.round(time_supermarket) + 'min'
}

var speedSlider = document.getElementById("speed-slider");
var speed = speedSlider.value;


function setSpeed(mode) {
    if(mode == "bike") {
        document.getElementById("speed-slider").value = 15;
    } else if(mode == "walk") {
        document.getElementById("speed-slider").value = 5;
    }
    showValue(document.getElementById("speed-slider").value);
}



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






function score(response) {
    console.log(response)
    data = response 

    time_uni =  ((data.home_uni/1000)/ speed) * 60
    time_center = ((data.home_center/1000)/ speed) * 60
    time_supermarket = ((data.home_supermarket/1000)/ speed) * 60

    let busClosest = document.getElementById('bus-closest')
    let busDistance = document.getElementById('bus-distance')

    let homeUni = document.getElementById('home-uni')
    let homeCenter = document.getElementById('home-center')
    let homeSupermarket = document.getElementById('home-supermarket')

    let bikeUni = document.getElementById('bike-uni')
    let bikeCenter = document.getElementById('bike-center')
    let bikeSupermarket = document.getElementById('bike-supermarket')

    let walkSupermarket = document.getElementById('walk-supermarket')
    let busHome = document.getElementById('bus-home')
    let address = document.getElementById('address')

    address.innerHTML = 'Address:' + data.address
    busClosest.innerHTML = 'Closest bus stop: ' + data.bus_closest_name
    busDistance.innerHTML = 'Distance fron bus top: ' + data.bus_stop_distance + 'm'
    
    homeUni.innerHTML = 'Distance from home to university: ' + data.home_uni + 'm'
    homeCenter.innerHTML = 'Distance from home to city center: ' + data.home_center + 'm'
    homeSupermarket.innerHTML = 'Distance from home to supermarket: ' + data.home_supermarket + 'm'

    bikeUni.innerHTML = 'time from home to university: ' + Math.round(time_uni)+ 'min'
    bikeCenter.innerHTML = 'time from home to city center: ' + Math.round(time_center) + 'min'
    bikeSupermarket.innerHTML = 'time from home to supermarket: ' + Math.round(time_supermarket) + 'min'
    // add marker to closest bus stop 
    L.marker([data.bus_closest_lat, data.bus_closest_lon]).addTo(map)
    L.marker([data.home_lat, data.home_lon]).addTo(map)

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