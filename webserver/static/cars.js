let carsDict = {};
let carsArray = [];
let carBlockSize = 20 * 1000;
let carBlocksRequested = [];
let pendingCarRequests = {}; // key=block, value=amount_pending

function insertCarBinarly(car) {
    let beginId = -1;
    let endId = carsArray.length;
    while (endId - beginId > 1) {
        const middleId = Math.floor((beginId+endId)/2);
        if (car.begin < carsArray[middleId].begin) {
            endId = middleId;
        } else {
            beginId = middleId;
        }
    }
    carsArray.splice(endId, 0, car);
}

function loadCar(carname, doneFunc) {
    $.ajax({
        type: 'GET',
        url: '/car/'+carname,
        success: (data) => {
            const csv = Papa.parse(data, {delimiter: ';', header: true, skipEmptyLines: true});
            const first = csv.data[0];
            const marker = new google.maps.Marker({
                position: {lat: parseFloat(first.latitude), lng: parseFloat(first.longitude)},
                map: map,
                title: carname,
                icon: {
                    url: "./static/images/redcar_purple_marker_32.png"
                }
            });
            let car = {
                name: carname,
                movement: csv.data,
                marker: marker,
                begin: csv.data[0].time,
                end: csv.data[csv.data.length-1].time
            };
            carsDict[carname] = car;
            insertCarBinarly(car);
            doneFunc(car);
        }
    });
}


function timeToBlock(time) {
    return Math.floor(time/carBlockSize);
}


function updateCars() {
    const center = camera.center;
    const block = timeToBlock(center);
    if (carBlocksRequested.includes(block)) {
        if (pendingCarRequests[block] === 0) {
            drawCars(carsOnTime(center), camera.center);
        }

    } else {
        getCarBlock(block, center);
    }
}

function carsOnTime(time) {
    let selectedCars = [];
    for (const car of carsArray) {
        if (car.begin <= time) {
            if (car.end > time) {
                selectedCars.push(car);
            }
        } else {
            return selectedCars;
        }
    }
    return selectedCars;
}

function drawCars(cars, time) {
    for (const car of cars) {
        if (time >= car.begin && time < car.end) {
            const position = interpolateMovementTime(car.movement, time);
            car.marker.setPosition(position);
        } else {
            console.log(time+' not available')
        }
    }
}

function drawCarsFromNames(carNames, time) {
    let cars = [];
    for (const carName of carNames) {
        cars.push(carsDict[carName])
    }
    drawCars(cars, time);
}

function interpolateMovementTime(movement, targetTime) {
    let beginId = -1;
    let endId = movement.length-1;
    while (endId - beginId > 1) {
        const middleId = Math.floor((beginId+endId)/2);
        if (targetTime < movement[middleId].time) {
            endId = middleId;
        } else {
            beginId = middleId;
        }
    }

    const timegap = movement[endId].time - movement[beginId].time;
    const timeDiffBegin = (targetTime - movement[beginId].time) / timegap;

    return new google.maps.LatLng(
        movement[beginId].latitude * (1-timeDiffBegin) + movement[endId].latitude * timeDiffBegin,
        movement[beginId].longitude * (1-timeDiffBegin) + movement[endId].longitude * timeDiffBegin
    );
}

function getCarBlock(block, time) {
    carBlocksRequested.push(block);

    $.ajax({
        type: 'GET',
        url: '/cars_around_block/'+block,
        dataType: 'json',
        success: (carNames) => {
            pendingCarRequests[block] = 0;
            let known = [];
            for (const carName of carNames) {
                if (carsDict[carName] === undefined) {
                    pendingCarRequests[block] += 1;
                    loadCar(carName, (car) => {
                        pendingCarRequests[block] -= 1;
                        drawCars([car], time);
                    });
                } else {
                    known.push(carName)
                }
            }
            drawCarsFromNames(known, time);
        }
    });
}