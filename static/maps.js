let map;
let availableIntersections;
let layouts = {};
let sensors = {};
const intersectionSelect = document.createElement('select');
intersectionSelect.classList.add('mapsControl');
intersectionSelect.onchange = function() {focus(this.value)}


function initMap() {
    // Initialize the google map
    map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 19,
        mapTypeId: 'satellite'
    });

    map.controls[google.maps.ControlPosition.TOP_CENTER].push(intersectionSelect);
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(datepicker);

    google.maps.event.addListenerOnce(map, 'idle', () => {
        setTimeout(() => {
            $("[src='https://maps.gstatic.com/mapfiles/api-3/images/google_white5.png']")[0].style.display = 'none';
        }, 1000)
    });
}

function getAvailableLayouts(doneFunc) {
    // Sets `availableLayouts` to an array of available layouts
    // This is done asynchronous, so give a doneFunc to execute when done
    $.ajax({
        type: 'GET',
        url: '/available_intersections',
        dataType: 'json',
        success: (data) => {
            availableIntersections = data;
            for (const name of data) {
                let intersection = document.createElement('option');
                intersection.text = name;
                intersectionSelect.add(intersection);
            }
            loadAvailableTimes();
            doneFunc();
        }
    });
}

function loadLayout(layoutName, doneFunc) {
    // Requests the layout from the server by name
    // This is done asynchronous, so give a doneFunc to execute when done
    $.ajax({
        type: 'GET',
        url: '/layout/'+layoutName,
        success: (data) => {
            layouts[layoutName] = data;
            doneFunc();
        }
    })
}

function createLaneNodeMarkers(layout) {
    // Creates a marker for each node of each lane in this layout
    // This serves no purpose so far, just a jumping off point for later when the lanes should be drawn
    const laneSetPath = ['topology', 'mapData', 'intersections', 'intersectionGeometry', 'laneSet']
    for (const lane of exs(layout, laneSetPath).children) {
        for (const nodeXY of exs(lane, ['nodes']).children) {
            const lat = exs(nodeXY, ['node-LatLon', 'lat']).innerHTML /10000000;
            const lon = exs(nodeXY, ['node-LatLon', 'lon']).innerHTML /10000000;
            const marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat, lon),
                map: map,
                visible: false
            });
        }
    }
}

function createSensors(layout) {
    // Create a sensor object for each sensor in the layout

    // CIpath = ControlledIntersection Path
    const CIpath = ['topology', 'controlData', 'controller', 'controlUnits', 'controlUnit', 'controlledIntersections']
    for (const sensor of exs(layout, CIpath.concat(['sensors'])).children) {
        let sensorObject = {
            display: function() {
                return exs(this.xml, ['name']).innerHTML;
            },
            xml: sensor
        }

        if (sensor.getElementsByTagName('geoShape').length !== 0) {
            // When a geoshape is available, draw it as a polyline
            let geoshapeCoordinates = [];
            for (const indexPoint of exs(sensor, ['geoShape']).children) {
                geoshapeCoordinates.push({
                    lat: exs(indexPoint, ['lat']).innerHTML /10000000,
                    lng: exs(indexPoint, ['long']).innerHTML /10000000
                });
            }
            const polyline = new google.maps.Polyline({
                path: geoshapeCoordinates,
                geodesic: true,
                strokeColor: "#FF0000",
                strokeOpacity: 1.0,
                strokeWeight: 2,
                map: map
            });
            polyline.addListener('click', () => {
                alert(sensorObject.display());
            });
            sensorObject.polyline = polyline

        } else {
            // When no geoshape is available draw the sensor position as a marker
            const lat = exs(sensor, ['sensorPosition', 'lat']).innerHTML /10000000;
            const lon = exs(sensor, ['sensorPosition', 'long']).innerHTML /10000000;
            const marker = new google.maps.Marker({
                    position: new google.maps.LatLng(lat, lon),
                    map: map,
                });
            marker.addListener('click', () => {
                alert(sensorObject.display());
            });
            sensorObject.marker = marker;
        }

        sensors[sensorObject.display()] = sensorObject;
    }
}

function focusIntersection(layoutName) {
    // Move the camera to center on this layout
    const refpoint = exs(layouts[layoutName], ['topology', 'mapData', 'intersections', 'intersectionGeometry', 'refPoint']);
    map.setCenter({
        lat: exs(refpoint, ['lat']).innerHTML /10000000,
        lng: exs(refpoint, ['long']).innerHTML /10000000
    })
}

// Get available intersection, load them and focus on the first one
getAvailableLayouts(() => {
    for (const intersection of availableIntersections) {
        loadLayout(intersection, () => {
            createLaneNodeMarkers(layouts[intersection]);
            createSensors(layouts[intersection]);
            focusIntersection(availableIntersections[0]);
        });
    }
});
