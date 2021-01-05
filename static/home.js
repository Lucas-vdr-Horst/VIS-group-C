let map;
let availableLayouts;
let layouts = {};
let sensors = [];

function initMap() {
    // Initialize the google map
    map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 19,
        mapTypeId: 'satellite'
    });
}

function getAvailableLayouts(doneFunc) {
    // Sets `availableLayouts` to an array of available layouts
    // This is done asynchronous, so give a doneFunc to execute when done
    $.ajax({
        type: 'GET',
        url: '/available_layouts',
        dataType: 'json',
        success: (data) => {
            availableLayouts = data;
            for (const name of data) {
                let intersection = document.createElement('option')
                intersection.text = name;
                document.getElementById('intersectionSelect').add(intersection)
            }
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

        sensors.push(sensorObject);
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

function focusLoadIntersection(layoutName) {
    // Load the layout if not already done, and focus the camera on it
    if (!(layoutName in layouts)) {
        loadLayout(layoutName, () => {
            createLaneNodeMarkers(layouts[layoutName]);
            createSensors(layouts[layoutName]);
            focusIntersection(layoutName)
        });
    } else {
        focusIntersection(layoutName)
    }
}

// Get available intersection and focusload the first one
getAvailableLayouts(() => {
    focusLoadIntersection(availableLayouts[0]);
});
