$(function() {
   getUserPackets(function(packetNames) {
       // success
       packetTable_clear();

       console.log(packetNames);
       for(var i = 0; i < packetNames.length; i++) {
           var packet = packetNames[i];
           var link = "<a href='index.php?packet_id="+ packet +"'>"+ packet +"</a>";
            packetTable_addRow(i, link);
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

$("#button_logout_user").click(function() {
    logoutUser(function() {
        //success
        // TODO redirect to index
        packetTable_clear();
        packetTable_addRow('-', "Logout successfull.");  
    }, function() {
        // failure
        packetTable_clear();
        packetTable_addRow('-', "Error logging out");       
    });
});

function packetTable_clear() {
    $('#table_user_packets > tbody').html("");
}

function packetTable_addRow(index, packetName) {
    $('#table_user_packets > tbody:last-child').append('<tr><th scope="row">' + index + '</th><td>' + packetName + '</td></tr>');
}