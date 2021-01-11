
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



let inputsBlocks = {} // key=intersection, value=Array<block>
let requesting = false;

function inputsStateSearch(time, blocks) {
    if (blocks.length === 0) {return undefined}
    const centerIndex = Math.floor(blocks.length/2);
    const centerBlock = blocks[centerIndex];
    if (time >= centerBlock.begin && time <= centerBlock.end) {
        return centerBlock;
    }
    if (blocks.length === 1) {
        return undefined;
    }
    if (time < centerBlock.begin) {
        return inputsStateSearch(time, blocks.slice(0, centerIndex));
    } else {
        return inputsStateSearch(time, blocks.slice(centerIndex+1));
    }
}

function addInputBlock(block, intersection) {
    let blocksIntersection = inputsBlocks[intersection];
    if (blocksIntersection.length === 0) {blocksIntersection.push(block); return}
    if (block.end <= blocksIntersection[0].begin) {blocksIntersection.splice(0, 0, block); return}
    if (block.begin >= blocksIntersection[blocksIntersection.length-1].end) {blocksIntersection.push(block); return}
    for (let i=0; i<blocksIntersection.length-1; i++) {
        if (block.begin >= blocksIntersection[i].end && block.end <= blocksIntersection[i+1].begin) {
            blocksIntersection.splice(i+1, 0, block);
            return;
        }
    }
}

function testAdd() {
    addInputBlock({begin: 1, end:50}, 'BOS210');
    addInputBlock({begin: 75, end:125}, 'BOS210');
    addInputBlock({begin: 200, end:250}, 'BOS210');
    addInputBlock({begin: 250, end:260}, 'BOS210');
    addInputBlock({begin: 350, end:360}, 'BOS210');
    addInputBlock({begin: 750, end:800}, 'BOS210');
}

function drawInputs(block, intersection) {
    block.state.forEach((state, index) => {
        const sensor = sensors[intersection][header_names[intersection][index]]
        if (sensor !== undefined) {
            sensor.updateMap(state);
        }
    });
}

function updateInputs() {
    const center = Math.round(camera.center/100)*100;
    for (const intersection of selectedIntersections) {
        const block = inputsStateSearch(center, inputsBlocks);
        if (block !== undefined) {
            drawInputs(center, intersection);
        } else {

        }
    }
}