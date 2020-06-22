document.addEventListener('DOMContentLoaded', () => {

    //connet to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

    socket.on('connect', () => {
        document.querySelector('#channel_button').onclick = () => {
            const selection = document.querySelector('#channel_input').value;
            socket.emit('submit channel', { 'selection': selection })
        };
    });

    socket.on('cast channel', data => {

        const channel = document.createElement('span');
        channel.innerHTML = `<a style="text-decoration: solid;
                            color: white; 
                            font-family: monospace;" href="#" ># ${data["selection"]}</a><br>`;
        document.querySelector('#list').append(channel);
    })
})