var tracking_server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/";

var subscribed_ids = new Set();
var socket = undefined;
var current_id;

var set = "#packet_id";
var butt = "#update_packet_button";

var stations = [{"vehicle": "envelope", "address": "????", "time": getDate("0")}];

$(function() {
    socket = io.connect('http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/packetStatus');//http://localhost:8001/
    
    socket.on('update', function (socketResponse) {
        console.log(current_id);
        console.log(socketResponse);
        if (current_id !== undefined && socketResponse.packet_id !== undefined && socketResponse.packet_id !== current_id) {
            serverReturned("Das Paket mit der ID " + socketResponse.packet_id + " wurde an einem neuen Standort registriert.", set, butt);
            return;
        }
        if (socketResponse.location === undefined) {
            addRow("envelope-o", $("#receiver_city").val(), socketResponse.deliveryTime, getReciver());
            serverReturned("Ihr Paket ist da, schauen Sie in ihren Briefkasten.", set, butt);
        } else {
            addRow(socketResponse.vehicle, socketResponse.location, socketResponse.time);
            serverReturned("Ihr Paket wurde soeben in " + socketResponse.location + " gemeldet!", set, butt);

        }
        showPathInMap(map, stations);
    });  
    
    // check if id is passed by url
    var urlId = getUrlParameter("packet_id");
    if(urlId !== undefined && urlId.length > 0) {
        current_id = urlId;
        trackPacketId(current_id);
    }
});

function trackPacketId(packetId) {
    waitOnServer(set, butt);
    $.get(tracking_server_url + "packetStatus/" + packetId, function (responseData) {
        initMap();
        
        //sender Adresse
        $("#sender_name").val(responseData.sender_name);
        $("#sender_street").val(responseData.sender_street);
        $("#sender_city").val(responseData.sender_city);
        $("#sender_zip").val(responseData.sender_zip);
        //reciver Adresse
        $("#receiver_name").val(responseData.receiver_name);
        $("#receiver_street").val(responseData.receiver_street);
        $("#receiver_city").val(responseData.receiver_city);
        $("#receiver_zip").val(responseData.receiver_zip);

        $("#size").val(responseData.size);
        $("#weight").val((responseData.weight + "").replace('.', ","));
        //Liste
        //Erste Spalte
        $("#regloc").text(responseData.sender_city);
        $("#regdate").text(getDate(responseData.registration_time));
        //Restliche Spalten
        removeRows();

        // TODO whole address, not only city
        stations = [{"vehicle": "envelope", "address": getAbsender(), "time": getDate(responseData.registration_time)}];

        var arrayLength = responseData.stations.length;
        for (var i = 0; i < arrayLength; i++) {
            var row = responseData.stations[i];
            addRow(row.vehicle, row.location, row.time);
        }
        //Letzte Spalte
        if (responseData.deliveryTime !== undefined) {
            addRow("envelope-o", responseData.receiver_city, responseData.deliveryTime, getReciver());
        }
        serverReturned("", set, butt);
        showPathInMap(map, stations);
        if (!subscribed_ids.has(packetId)) {
            subscribed_ids.add(packetId);
            socket.emit('subscribe', {packet_id: packetId});
        }
    })
    .done(function () {
    })
    .fail(function (xhr, status, error) {
        failReturned(xhr.responseText, xhr.status, set, butt);
    })
    .always(cleanUp);
}

$("#search_id").submit(function () {   
    current_id = $("#packet_id").val();
    trackPacketId(current_id);
    return false;
});

//int/String/String/String
function addRow(symbol, loca, date, address) {
    var date = getDate(date);
    if (address === undefined)
        address = loca;
    stations.push({"vehicle": symbol, "address": address, "time": date});
    $('#Nachverfolgung > tbody:last-child').append('<tr name="addedRow"><th scope="row">' + stations.length + '</th><td><i class="' + iconMap(symbol) + '"></i></td><td>' + loca + '</td><td>' + date + '</td></tr>');
}
function removeRows() {
    $("[name='addedRow']").remove();
}

function getDate(date) {
    if (date.toString().includes("/")) {
        return date;
    } else {
        var date = new Date(parseInt(date) * 1000);
        var text = "";
        var x = date.getDate();
        if (x < 10) {
            text += "0";
        }
        text += x + ".";
        x = date.getMonth() + 1;
        if (x < 10) {
            text += "0";
        }
        text += x + "." + date.getFullYear() + " ";
        x = date.getHours();
        if (x < 10) {
            text += "0";
        }
        text += x + ":";
        x = date.getMinutes();
        if (x < 10) {
            text += "0";
        }
        text += x;
        return text;
    }
    return false;
}

//Sichtbarkeit ändern
function waitOnServer(fset, pbutton) {
    $(fset).prop("disabled", true);
    $(pbutton).prop("hidden", true);
    $("#spinner").prop("hidden", false);
    $("#meta_form").prop("hidden", true);
    clearMessage();
}
function serverReturned(info, fset, pbutton) {
    console.log("Request successful");
    $(fset).prop("disabled", false);
    $(pbutton).prop("hidden", false);
    $("#meta_form").prop("hidden", false);    
    
    if(info !== undefined && info.length > 0) {
        infoMessage(info);
    }
}
function failReturned(error, status, fset, pbutton) {
    console.log("error " + status);
    $(fset).prop("disabled", false);
    $(pbutton).prop("hidden", false);
    var errortext = "Ups. Etwas ist schief gegangen. ";
    if (error === undefined) {
        errortext += "Der Server reagiert nicht. Überprüfen Sie ihr Internetverbindung und versuchen Sie es später nochmal.";
    } else if (status === 404) {

        errortext = "Diese ID exitiert nicht.";

    }/**else if(statu == 504){
     errortext +="Der Server meldet einen Fehler 504. Versuchen Sie es später nochmal.";
     }*/ else {
        errortext += error;
    }
    
    errorMessage(errortext);
}
function cleanUp() {
    $("#spinner").prop("hidden", true);
}
function iconMap(hash) {
    if (hash === "envelope")
        return "fa fa-envelope-o";
    if (hash === "envelope-o")
        return "fa fa-envelope-open-o";
    if (hash === "center")
        return "fa fa-building-o";
    if (hash === "car")
        return "fa fa-car";
    if (hash === "foot")
        return "fa fa-bicycle";
    if (hash === "plane")
        return "fa fa-plane";
    if (hash === "rocket")
        return "fa fa-rocket";
    if (hash === "ship")
        return "fa fa-ship";
    if (hash === "train")
        return "fa fa-subway";
    if (hash === "truck")
        return "fa fa-truck";
    if (hash === "failed")
        return "fa fa-frown-o";
}
function getAbsender() {
    return $("#sender_zip").val() + " " + $("#sender_city").val() + ", " + " " + $("#sender_street").val();
}
function getReciver() {
    return $("#receiver_zip").val() + " " + $("#receiver_city").val() + ", " + " " + $("#receiver_street").val();
}