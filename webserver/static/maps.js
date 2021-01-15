let map;
let availableIntersections;
let selectedIntersections;
let layouts = {};
let sensors = {};
let lanes = {};
const intersectionSelect = document.createElement('select');
intersectionSelect.classList.add('mapsControl');
intersectionSelect.onchange = function() {focusIntersection(this.value)};
let lineSymbol;
const drawOffset = [0.000013, 0.0];


function initMap() {
    // Initialize the google map
    map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 19,
        mapTypeId: 'satellite'
    });

    map.controls[google.maps.ControlPosition.TOP_CENTER].push(intersectionSelect);
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(datepicker);

    // google.maps.event.addListenerOnce(map, 'idle', () => {
    //     setTimeout(() => {
    //         $("[src='https://maps.gstatic.com/mapfiles/api-3/images/google_white5.png']")[0].style.display = 'none';
    //     }, 1000)
    // });
    lineSymbol = {path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW};

    // Drawing Manager
    const drawingManager = new google.maps.drawing.DrawingManager({
        markerOptions: {
          icon:
            "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
        },
        map: map
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

                inputsBlocks[name] = [];
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
        let points = []
        for (const nodeXY of exs(lane, ['nodes']).children) {
            const lat = exs(nodeXY, ['node-LatLon', 'lat']).innerHTML /10000000 + drawOffset[0];
            const lon = exs(nodeXY, ['node-LatLon', 'lon']).innerHTML /10000000 + drawOffset[1];
            points.push({lat:lat, lng:lon})
        }

        const polyline = new google.maps.Polyline({
                path: points,
                icons: [{
                    icon: lineSymbol,
                    offset: '100%'
                }],
                geodesic: true,
                strokeColor: "orange",
                strokeOpacity: 1.0,
                strokeWeight: 2,
                map: map
            });
        polyline.addListener('click', () => {
                console.log(new XMLSerializer().serializeToString(lane));
            });
    }
}

function createSensors(layoutName) {
    // Create a sensor object for each sensor in the layout

    const layout = layouts[layoutName]
    // CIpath = ControlledIntersection Path
    const CIpath = ['topology', 'controlData', 'controller', 'controlUnits', 'controlUnit', 'controlledIntersections']
    let layoutSensors = {};
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
                    lat: exs(indexPoint, ['lat']).innerHTML /10000000 + drawOffset[0],
                    lng: exs(indexPoint, ['long']).innerHTML /10000000 + drawOffset[1]
                });
            }
            const polyline = new google.maps.Polygon({
                path: geoshapeCoordinates,
                geodesic: true,
                fillColor: "blue",
                strokeOpacity: 1.0,
                fillOpacity: 0.9,
                strokeWeight: 2,
                map: map
            });
            polyline.addListener('click', () => {
                alert(sensorObject.display());
            });
            sensorObject.polyline = polyline;
            sensorObject.updateMap = function(state) {
                let color;
                if (state === '|') {
                    color = 'green';
                } else {
                    color = 'red';
                }
                this.polyline.setOptions({fillColor: color})
            }

        } else {
            // When no geoshape is available draw the sensor position as a marker
            const lat = exs(sensor, ['sensorPosition', 'lat']).innerHTML /10000000 + drawOffset[0];
            const lon = exs(sensor, ['sensorPosition', 'long']).innerHTML /10000000 + drawOffset[1];
            const marker = new google.maps.Marker({
                    position: new google.maps.LatLng(lat, lon),
                    map: map,
                    title: sensorObject.display(),
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                    }
                });
            marker.addListener('click', () => {
                alert(sensorObject.display())
            });
            sensorObject.marker = marker;
            sensorObject.updateMap = function(state) {
                let color;
                if (state === '|') {
                    color = 'green';
                } else {
                    color = 'red';
                }
                this.marker.setOptions({icon: {url: "http://maps.google.com/mapfiles/ms/icons/"+color+"-dot.png"}})
            }
        }

        layoutSensors[sensorObject.display()] = sensorObject;
    }
    sensors[layoutName] = layoutSensors;
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
    selectedIntersections = availableIntersections;
    for (const intersection of selectedIntersections) {
        loadLayout(intersection, () => {
            createLaneNodeMarkers(layouts[intersection]);
            createSensors(intersection);
            focusIntersection(availableIntersections[0]);
        });
        requested[intersection] = 0;
    }
});
