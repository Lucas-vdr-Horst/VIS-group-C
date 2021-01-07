
let loadRange = 10 * 1000;  // 10 seconds
let sensorStatesOnTime = {}; // key=datetime in miliseconds,  value=dict(key=sensorname, value=state)
let carStatesOnTime = {};
let timesRequested = [];

function updateDynamics() {
    const timeframeWanted = {begin: camera.center-loadRange, end: camera.center+loadRange};
    const resized = resizeTimeframeByKnown(timeframeWanted);
    if (resized.begin === resized.end) {
        drawSensors(camera.center);
    } else {

    }
}

function drawSensors(time) {
    const sensorStates = sensorStatesOnTime[time];
    Object.keys(sensorStates).forEach(function(sensorName) {
        sensors[sensorName].updateMap(sensorStates[sensorName]);
    });
}

function resizeTimeframeByKnown(timeframe) {
    let newTimeframe = timeframe;
    for (const requested of timesRequested) {
        if (requested.end > newTimeframe.begin && requested.begin < newTimeframe.begin) {
            newTimeframe.begin = requested.end;
        } else if (requested.begin < newTimeframe.end && requested.end > newTimeframe.end) {
            newTimeframe.end = requested.begin;
        }
        if (newTimeframe.begin > newTimeframe.end) {
            return {begin: 0, end: 0};
        }
    }
    return newTimeframe
}

function requestTimeframe(timeframe) {
    timesRequested.push(timeframe);
    $.ajax({
        type: 'GET',
        url: '/sensor_timeframe/'+JSON.stringify(timeframe),
        dataType: 'json',
        success: (data) => {
            console.log(data);
        }
    });
}
