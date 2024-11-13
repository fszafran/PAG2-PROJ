let xStart=NaN, yStart=NaN, xEnd=NaN, yEnd=NaN;
let startMarker = NaN;
let endMarker = NaN;
let m = L.map('m').setView([53.0138, 18.5984], 13);
let route = L.layerGroup().addTo(m);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(m);

window.xStart = xStart;
window.yStart = yStart;
window.xEnd = xEnd;
window.yEnd = yEnd;

function transform4326To2180(lat, lng){
    const sourceCoordinateSystem = 'EPSG:4326';
    const targetCoordinateSystem = '+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs';
    return proj4(sourceCoordinateSystem, targetCoordinateSystem, [lng, lat]);
}

function updateMarker(marker, latlng, pointType) {
    let XY = transform4326To2180(latlng.lat, latlng.lng);
    let x = XY[1];
    let y = XY[0];
    marker.setLatLng(latlng);
    marker.getPopup().setContent(`<b>${pointType === 'start' ? 'Punkt początkowy' : 'Punkt końcowy'}:</b><br>X: ${x}<br>Y: ${y}`).openOn(m);
    if (pointType === 'start') {
        xStart = x;
        yStart = y;
        window.xStart = xStart;
        window.yStart = yStart;
        console.log(`Start point set to: ${xStart}, ${yStart}`);
    } else {
        xEnd = x;
        yEnd = y;
        window.xEnd = xEnd;
        window.yEnd = yEnd;
        console.log(`End point set to: ${xEnd}, ${yEnd}`);

    }
}

m.addEventListener('click', function(e) {
    const pointType = document.querySelector('input[name="pointType"]:checked').value;
    let lat = e.latlng.lat;
    let lng = e.latlng.lng;
    let XY = transform4326To2180(lat, lng);
    if (pointType === 'start') {
        if (startMarker) {
            m.removeLayer(startMarker);
        }
        xStart = XY[1];
        yStart = XY[0];
        window.xStart = xStart;
        window.yStart = yStart;
        console.log(`Start point set to: ${xStart}, ${yStart}`);
        startMarker = L.marker([lat, lng], { draggable: true }).addTo(m);
        startMarker.bindPopup(`<b>Punkt początkowy:</b><br>X: ${xStart}<br>Y: ${yStart}`).openPopup();
        startMarker.on('dragend', function(event) {
            let marker = event.target;
            let position = marker.getLatLng();
            updateMarker(marker, position, 'start');
        });
        startMarker.on('dblclick', function(event){
            let marker = event.target;
            m.removeLayer(marker);
        });
    } else if (pointType === 'end') {
        if (endMarker) {
            m.removeLayer(endMarker);
        }
        xEnd = XY[1];
        yEnd = XY[0];
        window.xEnd = xEnd;
        window.yEnd = yEnd;
        
        console.log(`End point set to: ${xEnd}, ${yEnd}`);
        endMarker = L.marker([lat, lng], { draggable: true }).addTo(m);
        endMarker.bindPopup(`<b>Punkt końcowy:</b><br>X: ${xEnd}<br>Y: ${yEnd}`).openPopup();
        endMarker.on('dragend', function(event) {
            let marker = event.target;
            let position = marker.getLatLng();
            updateMarker(marker, position, 'end');
        });
        endMarker.on('dblclick', function(event){
            let marker = event.target;
            m.removeLayer(marker);
        });
    }
});

function drawPath(newValue) {
    // route.eachLayer(function (layer) {
    //     route.removeLayer(layer);
    // });
    // route.clearLayers();
    for (let i = 0; i < newValue.length; i++) {
        let part = newValue[i];
        L.polyline(part).addTo(route);
    }
}

let inputBox = document.querySelector("#pathPartsInput");

observeElement(inputBox, "value", function (oldValue, newValue) {
    drawPath(JSON.parse(newValue));
});

function observeElement(element, property, callback, delay = 0) {
    let elementPrototype = Object.getPrototypeOf(element);
    if (elementPrototype.hasOwnProperty(property)) {
        let descriptor = Object.getOwnPropertyDescriptor(elementPrototype, property);
        Object.defineProperty(element, property, {
            get: function() {
                return descriptor.get.apply(this, arguments);
            },
            set: function () {
                let oldValue = this[property];
                descriptor.set.apply(this, arguments);
                let newValue = this[property];
                if (typeof callback == "function") {
                    setTimeout(callback.bind(this, oldValue, newValue), delay);
                }
                return newValue;
            }
        });
    }
}
