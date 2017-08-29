var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8002/";
//var server_url = "http://bla.bla:8001/";

var query_register_user = "add_user";
var query_login_user = "authenticate_user";
var query_delete_user = "delete_user";
var query_add_packet_to_user = "add_packet_to_user";
var query_get_user_packets = "get_packets_from_user";

$("#register_button").click(function() {
    register_email = $("#register_email").val();
    register_password = $("#register_password").val();
    
    registerUser(register_email, register_password, function() {
        //success
        console.log("Registering user successfully.");
    }, function() {
        //failure
        console.log("Error registering user");
    });
});

function writeSessioIdCookie(serverResponseJson) {
    if("session_id" in serverResponseJson) {
        var sessionId = serverResponseJson['session_id']
        console.log("session id: " + sessionId);
    } else {
        console.log("session id not found in response.");
        return;
    }

    var exmins = 30;
    var d = new Date();
    d.setTime(d.getTime() + (exmins*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = "session_id=" +sessionId + ";" + expires + ";path=/";
}

function readSessionIdCookie() {
    var name = "session_id=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');

    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }

    return undefined;
}

function registerUser(email, password, successCallback, failureCallback) {  
    if(!email || !password) {
        console.log("Email or password not provided.");
        return;
    }
    
    var query = server_url + query_register_user;
    console.log("query: " + query);
    
    var data = {"email" : email,
		"password" : password};
    
    $.post(query, data, function(responseText) {
        console.log("query: response");
        
        var obj = JSON.parse(responseText);
        console.log("response: " + obj);
		
        successCallback();
      })
      .done(function() {
        console.log("query: done");
      })
      .fail(function(xhr, status, error) {
        console.log("query: fail");
        failureCallback();
	 });
}

function loginUser(email, password, successCallback, failureCallback) {
    if(!email || !password) {
        console.log("Email or password not provided.");
        return;
    }
    
    var query = server_url + query_login_user;
    console.log("query: " + query);
       
    var requestData = {"email" : email,
		"password" : password};   
    
    /*$.ajax(query, {
     method: 'POST',
     data: data,
     crossDomain: true,
     success: function(xhr, status, error) {
        console.log("query: response");
        successCallback();
		
      }, error: function() {
        console.log("query: fail");
        failureCallback();
	 }});*/
    
    console.log("query: " + query);

    $.post(query, requestData, function(data) {
        console.log("query done: " + data);
        writeSessioIdCookie(data);
        successCallback();
      });
}

function addPacketToUser(packetId, successCallback, failureCallback)
{
    var query = server_url + query_add_packet_to_user;
    console.log("query: " + query);
    
    var data = {"packet" : packetId};
    
    $.post(query, data, function(responseText) {
        console.log("query: response");
        successCallback();
		
      })
      .done(function() {
        console.log("query: done");
      })
      .fail(function(xhr, status, error) {
        console.log("query: fail");
        failureCallback();
	 });
}

function deleteUser(successCallback, failureCallback)
{
    var query = server_url + query_delete_user;
    console.log("query: " + query);
    
    $.post(query, function(responseText) {
        console.log("query: response");
        successCallback();
		
      })
      .done(function() {
        console.log("query: done");
      })
      .fail(function(xhr, status, error) {
        console.log("query: fail");
        failureCallback();
	 });
}

function getUserPackets(successCallback, failureCallback) 
{
    var query = server_url + query_get_user_packets;
    console.log("query: " + query);
    
    $.ajax(query, {
     method: 'GET',
     xhrFields: { withCredentials: true },
     crossDomain: true,
     success: function(response) {
        console.log("query: response");
        
        //var obj = JSON.parse(responseText);
        console.log("response: " + response);
        
        // dummy answer
        var packets = ["packet1", "packet2"];
        successCallback(packets);
		
      },
     error: function() {
        console.log("query: fail");
        failureCallback();
	 }
  });
}
