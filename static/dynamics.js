
let sensorStatesOnTime = {}; // key=datetime in miliseconds,  value=dict(key=intersection, value=Array[states])
let header_names = {}; // key=intersection, value=Array[names]

$.ajax({
    type: 'GET',
    url: '/header_names',
    dataType: 'json',
    success: (data) => {header_names = data}
});

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


let inputsBlocks = {}; // key=intersection, value=Array<block>
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
    if (blocksIntersection.length === 0) {blocksIntersection.push(block)} else {
        if (block.end <= blocksIntersection[0].begin) {blocksIntersection.splice(0, 0, block)} else {
            if (block.begin >= blocksIntersection[blocksIntersection.length-1].end) {blocksIntersection.push(block)} else {
                for (let i=0; i<blocksIntersection.length-1; i++) {
                    if (block.begin >= blocksIntersection[i].end && block.end <= blocksIntersection[i+1].begin) {
                        blocksIntersection.splice(i+1, 0, block);
                        break;
                    }
                }
            }
        }
    }

    // Adding the visual block
    const left = (block.begin - block_ref_time) / camera.zoom * 100;
    const width = (block.end - block.begin) / camera.zoom * 100;
    $('#loaded_blocks').append("<div class='known_block' style='left:"+left+"%; width:"+width+"%'></div>");
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
        let block = inputsStateSearch(center, inputsBlocks[intersection]);
        if (block !== undefined) {
            drawInputs(block, intersection);
        } else {
            requestBlock(center, intersection, () => {
                block = inputsStateSearch(center, inputsBlocks[intersection]);
                drawInputs(block, intersection);
            })
        }
    }
}

let requested = {};

function requestBlock(time, intersection, doneFunc) {
    if (requested[intersection] < 1 && timeAvailable(time)) {
        requested[intersection] += 1;
        $.ajax({
            type: 'GET',
            url: '/sensor_blocks',
            data: {intersection: intersection, time: time},
            dataType: 'json',
            success: (data) => {
                requested[intersection] -= 1;
                for (const block of data) {
                    if (inputsStateSearch(block.begin, inputsBlocks[intersection]) === undefined) {
                        block.state = block.state.split(';')
                        addInputBlock(block, intersection);
                    }
                }
                doneFunc();
            }
        });
    }
}

function timeAvailable(time) {
    for (const line of availableLines) {
        if (time > line.getAttribute('begintime') && time < line.getAttribute('endtime')) {return true}
    }
    return false;
}