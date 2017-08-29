//var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8002/";
var server_url = "http://localhost:8002/";

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
       
    var data = {"email" : email,
		"password" : password};
    
    
    $.ajax(query, {
     method: 'POST',
     data: data,
     crossDomain: true,
     success: function(xhr, status, error) {
        console.log("query: response");
        successCallback();
		
      }, error: function() {
        console.log("query: fail");
        failureCallback();
	 }});
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
