
const camera = {
    center: 0,
    zoom: 10
}

let tl = $('#timeline');

function updateTimeline() {
    let elements = tl[0].getElementsByClassName('td');
    while (elements[0]) {
        elements[0].parentNode.removeChild(elements[0])
    }

    for (let i=0; i<15; i++) {
        const td = document.createElement('p');
        td.innerText = Math.round(camera.center*camera.zoom) + i - camera.zoom/2 + '';
        td.classList.add('td');
        td.style.left = (td.innerText / camera.zoom - camera.center + 0.5) * 100 + '%';
        tl[0].appendChild(td)
    }
}

tl.mousedown(function (e) {
    camera.oldCenter = camera.center;
    camera.startDrag = e.originalEvent.clientX / window.innerWidth;
    tl.css('cursor', 'grabbing');
});

tl[0].onmousemove = function(e) {
    if (camera.startDrag !== undefined) {
        camera.center = camera.oldCenter + camera.startDrag - e.clientX / window.innerWidth;
        updateTimeline();
    }
};

function release() {
    camera.startDrag = undefined;
    tl.css('cursor', 'grab');
}

$(document).mouseup(release);

updateTimeline();