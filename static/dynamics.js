
let sensorStatesOnTime = {}; // key=datetime in miliseconds,  value=dict(key=intersection, value=Array[states])
let header_names = {}; // key=intersection, value=Array[names]
let carStatesOnTime = {};

$.ajax({
    type: 'GET',
    url: '/header_names',
    dataType: 'json',
    success: (data) => {header_names = data}
})


function loadUpdate() {
    const center = Math.round(camera.center/100)*100;
    if (sensorStatesOnTime[center] !== undefined) {
        displayUpdate(center, 'known');
    } else {
        requestTimeframe(center-200, () => {
            displayUpdate(center, 'loaded');
        });
    }
}






// function updateDynamics() {
//     const center = Math.round(camera.center/100)*100;
//     const timeframeWanted = {begin: center-loadRange, end: center+loadRange};
//     const resized = resizeTimeframeByKnown(timeframeWanted);
//     if (resized.begin === resized.end) {
//         drawSensors(center);
//     } else {
//         console.log(resized);
//     }
// }

function displayUpdate(time, type) {
    const sensorStates = sensorStatesOnTime[time];
    if (sensorStates === undefined) {console.log('error time '+time+'. type: '+type)}
    for (const intersection of availableIntersections) {
        if (sensorStates[intersection] !== undefined) {
            sensorStates[intersection].forEach((state, index) => {
                const sensor = sensors[intersection][header_names[intersection][index]]
                if (sensor !== undefined) {
                    sensor.updateMap(state);
                }
            })
        }
    }
}

// function drawSensors(time) {
//     const sensorStates = sensorStatesOnTime[time];
//     Object.keys(sensorStates).forEach(function(intersection) {
//         Object.keys(sensorStates[intersection]).forEach(function (sensorName) {
//             if (sensors[intersection][sensorName] !== undefined) {
//                 sensors[intersection][sensorName].updateMap(sensorStates[intersection][sensorName]);
//             } else {console.log('sensor '+sensorName+' on intersection '+intersection+' not found')}
//         })
//     });
// }
//
// function resizeTimeframeByKnown(timeframe) {
//     let newTimeframe = timeframe;
//     for (const requested of timesRequested) {
//         if (requested.end > newTimeframe.begin && requested.begin < newTimeframe.begin) {
//             newTimeframe.begin = requested.end;
//         } else if (requested.begin < newTimeframe.end && requested.end > newTimeframe.end) {
//             newTimeframe.end = requested.begin;
//         }
//         if (newTimeframe.begin > newTimeframe.end) {
//             return {begin: 0, end: 0};
//         }
//     }
//     return newTimeframe
// }

function requestTimeframe(time, doneFunc) {
    $.ajax({
        type: 'GET',
        url: '/sensor_block/'+time,
        dataType: 'json',
        success: (data) => {
            Object.keys(data).forEach(intersection=> {
                data[intersection].forEach((line, i) => {
                    if (sensorStatesOnTime[time+i*100] === undefined) {
                        sensorStatesOnTime[time+i*100] = {};
                    }
                    sensorStatesOnTime[time+i*100][intersection] = line.split(';');
                })
            });
            doneFunc();
        }
    });
}
