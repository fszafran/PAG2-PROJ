let xStart=NaN, yStart=NaN, xEnd=NaN, yEnd=NaN;
let startMarker = NaN;
let endMarker = NaN;
let inputBox = document.querySelector("#pathPartsInput");

let m = L.map('m').setView([53.0138, 18.5984], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(m);

let route = L.layerGroup().addTo(m);

window.xStart = xStart;
window.yStart = yStart;
window.xEnd = xEnd;
window.yEnd = yEnd;

m.addEventListener('click', function(e) {
    route.clearLayers();
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
        startMarker = L.marker([lat, lng], { draggable: true }).addTo(m);
        geocode(lat, lng, function(address) {
            startMarker.bindPopup(createPopupContent(pointType, xStart, yStart, address)).openPopup();
        });
        setupMarkerEvents(startMarker, 'start');

    } else if (pointType === 'end') {
        if (endMarker) {
            m.removeLayer(endMarker);
        }
        xEnd = XY[1];
        yEnd = XY[0];
        window.xEnd = xEnd;
        window.yEnd = yEnd;
        
        endMarker = L.marker([lat, lng], { draggable: true }).addTo(m);
        geocode(lat, lng, function(address) {
            endMarker.bindPopup(createPopupContent(pointType, xEnd, yEnd, address)).openPopup();
        });
        setupMarkerEvents(endMarker, 'end');
    }
});

function transform4326To2180(lat, lng){
    const sourceCoordinateSystem = 'EPSG:4326';
    const targetCoordinateSystem = '+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs';
    return proj4(sourceCoordinateSystem, targetCoordinateSystem, [lng, lat]);
}

function geocode(lat, lng, callback) {
    L.Control.Geocoder.nominatim().reverse(
        { lat: lat, lng: lng },
        m.options.crs.scale(m.getZoom()),
        function(results) {
            let result = results[0];
            if (result) {
                callback(result.name);
            } else {
                callback("Adres nieznaleziony");
            }
        }
    );
}

function createPopupContent(pointType, x, y, address){
    return `
        <div class="popup-content">
            <b>${pointType === 'start' ? 'Punkt początkowy' : 'Punkt końcowy'}:</b><br>
            <b>Adres:</b> <span class="address">${address}</span><br>
            <b>X:</b> <span class="coordinate">${x.toFixed(2)} m</span><br>
            <b>Y:</b> <span class="coordinate">${y.toFixed(2)} m</span><br>
        </div>
    `;
}

function updateCoords(pointType, x, y){
    if (pointType === 'start') {
        xStart = x;
        yStart = y;
        window.xStart = xStart;
        window.yStart = yStart;
    } else {
        xEnd = x;
        yEnd = y;
        window.xEnd = xEnd;
        window.yEnd = yEnd;
    }
}

function setupMarkerEvents(marker, pointType) {
    marker.on('dragend', function(event) {
        let theMarker = event.target;
        let position = marker.getLatLng();
        updateMarker(theMarker, position, pointType);
    });
    marker.on('dblclick', function(event){
        let theMarker = event.target;
        m.removeLayer(theMarker);
        route.clearLayers();
        updateCoords(pointType, NaN, NaN);
    });     
}

function updateMarker(marker, latlng, pointType) {
    route.clearLayers();
    let XY = transform4326To2180(latlng.lat, latlng.lng);
    let x = XY[1];
    let y = XY[0];
    marker.setLatLng(latlng);
    geocode(latlng.lat, latlng.lng, function(address) {
        marker.getPopup().setContent(createPopupContent(pointType, x, y, address)).openOn(m);
    });    
    updateCoords(pointType, x, y);
}

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

observeElement(inputBox, "value", function (oldValue, newValue) {
    drawPath(JSON.parse(newValue));
});

function drawPath(newValue) {
    route.clearLayers();
    m.closePopup();

    let latLngs = [];
    for (let i = 0; i < newValue.length; i++) {
        let part = newValue[i];
        latLngs = latLngs.concat(part);
        L.polyline(part, {color: '#007FFF', weight: 5}).addTo(route);
    }

    let bounds = L.latLngBounds(latLngs);
    m.fitBounds(bounds, {padding: [30,30]});
}

function clearMap() {
    route.clearLayers();

    if (startMarker) {
        m.removeLayer(startMarker);
        startMarker = null;
    }
    if (endMarker) {
        m.removeLayer(endMarker);
        endMarker = null;
    }

    xStart = NaN;
    yStart = NaN;
    xEnd = NaN;
    yEnd = NaN;
    window.xStart = xStart;
    window.yStart = yStart;
    window.xEnd = xEnd;
    window.yEnd = yEnd;

    path_parts = [];
    const pathPartsInput = document.getElementById("pathPartsInput");
    pathPartsInput.value = JSON.stringify([]);
}
document.getElementById("clearMapButton").addEventListener("click", clearMap);