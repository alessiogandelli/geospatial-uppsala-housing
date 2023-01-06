
path = '/Users/alessiogandelli/dev/uni/geospatial-uppsala-housing/data/uppsalaGeoJSON/'
let busRoutes;
let stopsCircles;
let supermarketCircles;

fetch('http://127.0.0.1:8000/routes')
    .then(response => response.json())
    .then(routes => {
        // add the bus routes layer
        busRoutes = L.geoJSON(routes).addTo(map);
    });


// import the GeoJSON file for bus stop

fetch('http://127.0.0.1:8000/stops')
  .then(response => response.json())
  .then(stops => {
    L.geoJSON(stops, {
      pointToLayer: function(feature, latlng) {
        return L.circle(latlng, {
          radius: 5,  // radius in meters
          color: 'green',
          fillColor: '#f03',
          fillOpacity: 0.5
        });
      },
      onEachFeature: function(feature, layer) {
        // add the name of the supermarket as a popup
        layer.bindPopup(feature.properties.name);
      }
    }).addTo(map);
  });

console.log(stopsCircles);

//import the GeoJSON file for supermarkets
// fetch('http://127.0.0.1:8000/supermarkets')
//     .then(response => response.json())
//     .then(supermarkets => {
//         // create an empty layer group for the supermarkets
//         supermarketCircles = L.layerGroup().addTo(map);

//         // loop through each feature in the GeoJSON object
//         supermarkets.features.forEach(feature => {
//             // get the coordinates of the feature
//             var coords = feature.geometry.coordinates;
//             // create a new circle at the coordinates
//             var circle = L.circle(coords, {
//                 radius: 100,  // radius in meters
//                 color: 'red',
//                 fillColor: '#f03',
//                 fillOpacity: 0.5
//             }).addTo(supermarketCircles);
//             // add the name of the supermarket as a popup
//             circle.bindPopup(feature.properties.name);
//         });
//     });

var map = L.map('map').setView([59.8586, 17.6389], 12);

// add the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// add the Lab location marker
var labLocation = L.marker([59.8586, 17.6389]).addTo(map);
labLocation.bindPopup("Ångströmlaboratoriet").openPopup();

// create a layer control and add it to the map
var layerControl = L.control.layers({}, {
    "Bus Routes": busRoutes
    //"Bus Stops": stopsCircles,
  //  "Supermarkets": supermarketCircles
}).addTo(map);









