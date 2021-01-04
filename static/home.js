let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map_canvas'), {
        center: { lat: 52.1326, lng: 5.2913 },
        zoom: 8
    });
}

let available_layouts

$.ajax({
    type: 'GET',
    url: '/available_layouts',
    dataType: 'json',
    success: (data) => {available_layouts = data;
        loadLayout(available_layouts[0]); //tmp for testing
    }
})

let x;

function loadLayout(layoutName) {
    $.ajax({
        type: 'GET',
        url: '/layout/'+layoutName,
        success: (data) => {
            x = data;

            const laneSetPath = ['topology', 'mapData', 'intersections', 'intersectionGeometry', 'laneSet']
            for (const lane of exs(data, laneSetPath).children) {
                for (const nodeXY of exs(lane, ['nodes']).children) {
                    const lat = exs(nodeXY, ['node-LatLon', 'lat']).innerHTML /10000000;
                    const lon = exs(nodeXY, ['node-LatLon', 'lon']).innerHTML /10000000;
                    const marker = new google.maps.Marker({
                        position: new google.maps.LatLng(lat, lon),
                        map: map
                    });
                }
            }
        }
    })
}
