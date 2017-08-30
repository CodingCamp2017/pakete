var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8002/";
//var server_url = "http://localhost:8002/";

var query_register_user = "add_user";
var query_login_user = "authenticate_user";
var query_delete_user = "delete_user";
var query_add_packet_to_user = "add_packet_to_user";
var query_get_user_packets = "get_packets_from_user";
var query_logout = "logout";

function registerUser(email, password, successCallback, failureCallback) {  
    if(!email || !password) {
        failureCallback("Email or password not provided.")
        return;
    }
    
    var query = server_url + query_register_user;    
    var requestData = {"email" : email, "password" : password};
    
    $.post(query, requestData, function(response) {     
        successCallback();
      })
      .fail(function(xhr, status, error) {
        failureCallback("Unable to register user.");
	 });
}

function loginUser(email, password, successCallback, failureCallback) {
    if(!email || !password) {
        failureCallback("Email or password not provided.");
        return;
    }
    
    var query = server_url + query_login_user;
    var requestData = {"email" : email, "password" : password};   
    
    $.post(query, requestData, function(response) {
        writeSessioIdCookie(response);
        successCallback();
    })
    .fail(function (xhr, status, error) {
        failureCallback("Login failed.");
    });
}

function addPacketToUser(packetId, successCallback, failureCallback)
{
    var query = server_url + query_add_packet_to_user;    
    
    var sessionId = readSessionIdCookie();
    if(sessionId !== undefined) {
        var requestData = {"packet": packetId, "session_id": sessionId};
        $.post(query, requestData, function (response) {
            successCallback();
        })
        .fail(function (xhr, status, error) {
            failureCallback("Adding packet failed.");
        });
    } else {
        failureCallback("User not logged in.");
        return;
    } 
}

function deleteUser(successCallback, failureCallback)
{
    var sessionId = readSessionIdCookie();
    if(sessionId !== undefined) {
        var query = server_url + query_delete_user;
        $.post(query, {"session_id": sessionId}, function (response) {
            clearSessionIdCookie();
            successCallback();
        })
        .fail(function (xhr, status, error) {
            failureCallback("Unable to delete user.");
        });
    }   
}

function getUserPackets(successCallback, failureCallback) 
{               
    var sessionId = readSessionIdCookie();
    if(sessionId !== undefined) {
        var query = server_url + query_get_user_packets + "/" + sessionId;
        $.get(query, function (responseData) {
            successCallback(responseData['packets']);
        });
    } else {
        failureCallback("User not logged in.");
        return;
    } 
}

function logoutUser(successCallback, failureCallback)
{
    var query = server_url + query_logout;

    var sessionId = readSessionIdCookie();
    if (sessionId !== undefined) {
        $.post(query, {'session_id': sessionId}, function (response) {
            clearSessionIdCookie();
            successCallback();
        })
        .fail(function (xhr, status, error) {
            failureCallback("Logging out user failed.");
        });
    } else {
        failureCallback("User not logged in.");
        return;
    }
}