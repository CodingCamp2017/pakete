var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8002/";
//var server_url = "http://168.192.168.66:80/";

var query_register_user = "add_user";
var query_login_user = "authenticate_user";
var query_add_packet_to_user = "add_packet_to_user";
var query_get_user_packets = "get_packets_from_user";

$("#register_button").click(function() {
    
    register_email = $("#register_email").val();
    register_password = $("#register_password").val();
        
    if(!register_email || !register_password) {
        console.log("Email or password not provided.");
        return;
    }
    
    var query = server_url + query_register_user;
    console.log("query: " + query);
    
    var data = {"email" : register_email,
		"password" : register_password};
    
    $.post(query, data, function(responseText) {
        console.log("query: response");
        
        var obj = JSON.parse(responseText);
        console.log("response: " + obj);
		
      })
      .done(function() {
        console.log("query: done");
      })
      .fail(function(xhr, status, error) {
        console.log("query: fail");
	 });
});

$("#login_button").click(function() {
    
    login_email = $("#register_email").val();
    login_password = $("#register_password").val();
        
    if(!login_email || !login_password) {
        console.log("Email or password not provided.");
        return;
    }
    
    var query = server_url + query_login_user;
    console.log("query: " + query);
    
    $.post(query, {email : register_email, password : register_password }, function(responseText) {
        console.log("query: response");
        
        var obj = JSON.parse(responseText);
        console.log("response: " + obj);
		
      })
      .done(function() {
        console.log("query: done");
      })
      .fail(function(xhr, status, error) {
        console.log("query: fail");
	 });
});