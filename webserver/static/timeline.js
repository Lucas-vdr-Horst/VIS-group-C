
const camera = {
    center: new Date(2020, 1, 6, 11, 35, 32, 0).getTime(),
    zoom: 60*1000
};
let block_ref_time;

let availableLines = [];

let tl = $('#timeline');
let ct = $('#center_time');
let amountInZoom = 10;

const datepicker = document.createElement('input');
datepicker.setAttribute('type', 'date');
datepicker.id = 'datepicker';
datepicker.classList.add('mapsControl');
datepicker.onchange = function() {
    camera.center = datepicker.valueAsDate.getTime();
    updateTimeline();
};

function updateTimeline() {
    let elements = tl[0].getElementsByClassName('td');
    while (elements[0]) {
        elements[0].parentNode.removeChild(elements[0])
    }

    for (let i=-amountInZoom/2; i<amountInZoom/2; i++) {
        const td = document.createElement('p');
        const roundMultiplier = camera.zoom/amountInZoom
        let mili = Math.round(camera.center/roundMultiplier)*roundMultiplier + i*camera.zoom/amountInZoom;
        td.innerText = new Date(mili).toLocaleTimeString('nl');
        //td.innerText = mili+'';
        td.classList.add('td');
        td.style.left = ((mili-camera.center) / (camera.zoom) + 0.5) * 100 + '%';
        tl[0].appendChild(td);
    }

    for (let line of availableLines) {
        line.style.left = ((line.getAttribute('beginTime')-camera.center) / (camera.zoom) + 0.5) * 100 + '%';
        line.style.width = (line.getAttribute('endTime') - line.getAttribute('beginTime')) / camera.zoom*200 + '%';
    }

    $('#loaded_blocks').css('left', ((block_ref_time-camera.center) / (camera.zoom) + 0.5) * 100 + '%');

    ct[0].innerText = new Date(camera.center).toString();
}

tl.mousedown(function (e) {
    camera.oldCenter = camera.center;
    camera.startDrag = e.originalEvent.clientX / window.innerWidth;
    tl.css('cursor', 'grabbing');
});

tl[0].onmousemove = function(e) {
    if (camera.startDrag !== undefined) {
        camera.center = camera.oldCenter + (camera.startDrag - e.clientX / window.innerWidth)*camera.zoom/amountInZoom*10;
        updateTimeline();
        datepicker.valueAsDate = new Date(camera.center + 60*60*1000);  // TODO: replace `+60*60*1000` with something timezone proper
        updateInputs();
        updateCars();
    }
};

function release() {
    camera.startDrag = undefined;
    tl.css('cursor', 'grab');
}

$(document).mouseup(release);

function loadAvailableTimes() {
    for (let intersection of availableIntersections) {
        $.ajax({
            type: 'GET',
            url: '/available_times/'+intersection,
            dataType: 'json',
            success: (data) => {
                const date = new Date((new Date(data[0][0]).getTime() + new Date(data[0][1]).getTime())/2)
                camera.center = date.getTime();
                datepicker.valueAsDate = date;
                for (let line of data) {
                    let availableLine = document.createElement('div');
                    availableLine.setAttribute('beginTime', new Date(line[0]).getTime()+'');
                    availableLine.setAttribute('endTime', new Date(line[1]).getTime()+'');
                    availableLine.classList.add('available_line');
                    tl[0].appendChild(availableLine);
                    availableLines.push(availableLine);
                }
                block_ref_time = availableLines[0].getAttribute('beginTime');
                updateTimeline();
                updateInputs();
            }
        })
    }
}

function setCenter(time) {
    camera.center = time;
    updateTimeline();
    datepicker.valueAsDate = new Date(camera.center + 60*60*1000);  // TODO: replace `+60*60*1000` with something timezone proper
    updateInputs();
    updateCars();
}
