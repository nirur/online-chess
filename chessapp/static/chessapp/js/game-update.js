// Continuous updating of board

// Initialize the connection to server
var connection = new WebSocket('ws://localhost:8000/ws/1');

// Add event listeners for when a move is processed by server and heartbeats from server
// Heartbeats are required, since the connection enters an 'inactive' state
// after 10 secs
connection.onmessage = function (initdata)
    {
    data = JSON.parse(initdata.data);
    switch (data['type']) {
        case 'HEARTBEAT':
            break;
        case 'MOVEPROCESSED':
            redrawSVG(data['data']);
            break;
    };
};

// Detector for when the current user makes a move
// jQuery dependencies are already included in the main HTML file
function clickDetector () {
    $('rect').click(
        function () {
            $(this).css('background-color', '#66ff66');
            let p1 = $(this).attr('class').slice(-2);
            $('rect').click(
                function () {
                    let p2 = $(this).attr('class').slice(-2);
                    let movestr = p1 + p2;
                    console.log(movestr)
                    connection.send(JSON.stringify({type:'MOVE', data:movestr}));
                }
            );
        }
    );
};

$(document).ready(
    clickDetector
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
connection.onopen = sendRepeatedly;
