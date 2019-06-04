$(document).ready(function () {

    var ip =  $('#ip').text();
    var recp = '';
    window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;   //compatibility for firefox and chrome
    var pc = new RTCPeerConnection({ iceServers: [] }), noop = function () { };

    pc.createDataChannel("");    //create a bogus data channel

    pc.createOffer(pc.setLocalDescription.bind(pc), noop);    // create offer and set local description

    pc.onicecandidate = function (ice) {  //listen for candidate events
        if (!ice || !ice.candidate || !ice.candidate.candidate) return;
        var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];
        //document.write('IP: ', myIP);   
        pc.onicecandidate = noop;
        ip = (myIP.split('.')[0] + myIP.split('.')[1] + myIP.split('.')[2]);

        if (ip == '1020105') {
            recp = 'Romulo Betancourt';
        }
        else if (ip == '102014') {
            recp = 'Romulo Betancourt';
        }
        else if (ip == '101100') {
            recp = '27 de Febrero';
        }
        else if (ip == '10114') {
            recp = '27 de Febrero';
        }
        else if (ip == '1030100') {
            recp = 'Megacentro';
        }

        $('.recp').html(recp);
        $('.sucursal').val(recp);

    };
});