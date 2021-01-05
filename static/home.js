let map;
let availableLayouts;
let layouts = {};

function initMap() {
    map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 19,
        mapTypeId: 'satellite'
    });
}

function getAvailableLayouts(doneFunc) {
    $.ajax({
        type: 'GET',
        url: '/available_layouts',
        dataType: 'json',
        success: (data) => {
            availableLayouts = data;
            doneFunc();
        }
    });
}

function loadLayout(layoutName, doneFunc) {
    $.ajax({
        type: 'GET',
        url: '/layout/'+layoutName,
        success: (data) => {
            layouts[layoutName] = data;
            const refpoint = exs(data, ['topology', 'mapData', 'intersections', 'intersectionGeometry', 'refPoint']);
            map.setCenter({
                lat: exs(refpoint, ['lat']).innerHTML /10000000,
                lng: exs(refpoint, ['long']).innerHTML /10000000
            })
            doneFunc();
        }
    })
}

function drawLaneNodes(layout) {
    const laneSetPath = ['topology', 'mapData', 'intersections', 'intersectionGeometry', 'laneSet']
    for (const lane of exs(layout, laneSetPath).children) {
        for (const nodeXY of exs(lane, ['nodes']).children) {
            const lat = exs(nodeXY, ['node-LatLon', 'lat']).innerHTML /10000000;
            const lon = exs(nodeXY, ['node-LatLon', 'lon']).innerHTML /10000000;
            const marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat, lon),
                map: map,
                //visible: false
            });
        }
    }
}

getAvailableLayouts(() => {
    const layoutName = availableLayouts[0];
    loadLayout(layoutName, () => {
        drawLaneNodes(layouts[layoutName]);
    });
});
