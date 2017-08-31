$(function() {
    getUserPackets(function(packetNames) {
        // success
        packetTable_clear();

        for (var i = 0; i < packetNames.length; i++) {
            var packet = packetNames[i];
            var link = "<a href='index.php?packet_id=" + packet + "'>" + packet + "</a>";
            packetTable_addRow(i, link);
        }
   }, function(message) {
        // failure
        packetTable_clear();
        errorMessage(message);
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

function packetTable_clear() {
    $('#table_user_packets > tbody').html("");
}

function packetTable_addRow(index, packetName) {
    $('#table_user_packets > tbody:last-child').append('<tr><th scope="row">' + index + '</th><td>' + packetName + '</td></tr>');
}