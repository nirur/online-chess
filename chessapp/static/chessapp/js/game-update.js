// Continuous updating of board

// Function to redraw the board

function redrawSVG(board_str) {
    let container = document.getElementById("svgContainer");
    container.innerHTML = board_str;
};

// Initialize the connection to server
var connection = new WebSocket('ws://'+window.location.hostname+':8000/ws/1');

// Add event listeners for when a move is processed by server and heartbeats from server
// Heartbeats are required, since the connection enters an 'inactive' state after 10 secs
connection.onmessage = function (rawdata) {
    data = JSON.parse(rawdata.data);
    switch (data['type']) {
        case 'HEARTBEAT':
            break;
        case 'PROCESSED':
            redrawSVG(data['data']);
            $('use').click(mainClickProcessor);
            break;
        case 'GAMEOVER':
            redrawSVG(data['data'][1]);
            let reason = document.getElementById('modal-reason');
            reason.innerHTML += data['data'][0];
            let modal = document.getElementById('modal');
            modal.style.display = 'block';
            break;
        case 'STREAM':
            document.getElementById('cam').srcObj = data['data'];
            break;
    };
};

// Detector for when the current user makes a move
// jQuery dependencies are already included in the main HTML file
var p1 = null;

function mainClickProcessor() {
    // Predefine 'pos' -- to keep 'pos' local when setting in if statement
    let pos = null;
    
    // Get the type of object that was clicked
    let typ = $(this).prop("nodeName");
    // Set 'pos' accordingly
    if (typ == 'rect') {
        pos = $(this).attr('class').slice(-2);
    }
    else if (typ == 'use') {
        let prevtype = $(this).prev().prop('nodeName');
        if (prevtype == 'rect') {
            pos = $(this).prev().attr('class').slice(-2);
        }
        else if (prevtype == 'use') {
            pos = $(this).prev().prev().attr('class').slice(-2);
        };
    };
    
    // Check if 'p1' is already defined
    // Send message to server accordingly
    if (p1 == null) {
        p1 = pos;
        connection.send(JSON.stringify({type:'PIECECLICK', data:p1}));
    }
    else {
        let movestr = p1 + pos;
        connection.send(JSON.stringify({type:'MOVE', data:movestr}));
        console.log(movestr);
        p1 = null;
    };
};

$(document).ready(
    function () {
        $('rect').click(mainClickProcessor);
        $('use').click(mainClickProcessor);
    }
);

// Heartbeats every 9.99 secs
// Gives system 0.1 secs to send the message
// Just being safe, since timeout is 10s and
// I don't want it to unexpectedly close
function sendRepeatedly () {
    if (connection.readyState != connection.CLOSED) {
        connection.send(JSON.stringify({type:'HEARTBEAT'}));
        setTimeout(sendRepeatedly, 9990);
    };
};
connection.onopen = function () {
    setTimeout(sendRepeatedly, 9990);
    navigator.mediaDevices.getUserMedia({video: true, audio: true})
        .then(function (stream) {connection.send(JSON.stringify({type: 'STREAM', data: stream}))})
        .catch(function (err) {connection.send(JSON.stringify({type: 'STREAM', data: null}))});
};
