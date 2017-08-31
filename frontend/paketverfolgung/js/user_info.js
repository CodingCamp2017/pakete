var tracking_server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/";

$(function() {
    getUserPackets(function(packetIds) {
        // success
        packetTable_clear();

        for (var i = 0; i < packetIds.length; i++) {
            var packet = packetIds[i];
            loadPacketInfo(i, packet);
        }
   }, function(message) {
        // failure
        packetTable_clear();
        errorMessage(message);
        
        packetTable_addRow("packetId", "sender", "receiver", "currentLocation");
   });
});

$("#add_packet_button").click(function() {
    var packetId = $("#add_packet_id").val();    
    addPacketToUser(packetId, function() {
        //success
        packetTable_clear();
        infoMessage("Packet added.");      
    }, function(message) {
        // failure
        packetTable_clear();
        errorMessage(message);       
    });
});

$("#button_delete_user").click(function() {
    deleteUser(function() {
        //success
        packetTable_clear();
        setLoginbarStatus();
        infoMessage("User deleted.");      
    }, function(message) {
        // failure
        packetTable_clear();
        errorMessage(message);      
    });
});

function loadPacketInfo(index, packetId) {
    $.get(tracking_server_url + "packetStatus/" + packetId, function (responseData) {        
        var sender = responseData.sender_name + ", " + responseData.sender_city;        
        var receiver = responseData.receiver_name + ", " + responseData.receiver_city;    
        var currentLocation = sender;
        
        if(responseData.stations !== undefined && responseData.stations.length > 0) {
            var currentLocationStation = responseData.stations[responseData.stations.length - 1];
            currentLocation = currentLocationStation.location;
        }
        
        packetTable_addRow(packetId, sender, receiver, currentLocation);
    })
    .fail(function (xhr, status, error) {
        console.log('error loading packetInfo, id: ' + packetId);
    });
}

function packetTable_clear() {
    $('#table_user_packets > tbody').html("");
}

function packetTable_addRow(packetId, sender, receiver, currentLocation) {
    var cols = '<td>' + sender + '</td>';
    cols = cols + '<td>' + receiver + '</td>';
    cols = cols + '<td><a href="index.php?packet_id=' + packetId + '">' + currentLocation +'</a></td>';
    cols = cols + '<td><button type="button" class="close" aria-label="Close"><span aria-hidden="true">&times;</span></button></td>';
    $('#table_user_packets > tbody:last-child').append('<tr>' + cols + '</tr>');
}