$(function() {
   getUserPackets(function(packetNames) {
       // success
       packetTable_clear();

       console.log(packetNames);
       for(var i = 0; i < packetNames.length; i++) {
            packetTable_addRow(i, packetNames[i]);
       }
   }, function() {
       // failure
       packetTable_clear();
       packetTable_addRow('-', "Error loading packets");
   });
});

$("#add_packet_button").click(function() {
    var packetId = $("#add_packet_id").val();
    
    addPacketToUser(packetId, function() {
        //success
        packetTable_clear();
       packetTable_addRow('-', "Packet added");
        
    }, function() {
        // failure
        packetTable_clear();
       packetTable_addRow('-', "Error adding packet");
        
    });
});

$("#button_delete_user").click(function() {
    deleteUser(function() {
        //success
        packetTable_clear();
       packetTable_addRow('-', "User deleted");
        
    }, function() {
        // failure
        packetTable_clear();
       packetTable_addRow('-', "Error deleting user");
        
    });
});

function packetTable_clear() {
    $('#table_user_packets > tbody').html("");
}

function packetTable_addRow(index, packetName) {
    $('#table_user_packets > tbody:last-child').append('<tr><th scope="row">' + index + '</th><td>' + packetName + '</td></tr>');
}