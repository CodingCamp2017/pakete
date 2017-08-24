var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/";
var query_register_user = "register";

//registration
$("#register_button").click(function() {
    
    email = $("#register_email").val();
    password = $("#register_password").val();
        
    if(!email || !password) {
        console.log("Email or password not provided.");
        return;
    }
    
    var query = server_url + query_register_user + "/" + email + "/" + password;
    console.log("query: " + query);
    
    $.get(query, function(responseText) {
        console.log("query: response");
        
        var obj = JSON.parse(responseText);
        //console.log(obj.someValue)
        
        //serverReturned(responseText,set,butt);
		
      })
      .done(function() {
        console.log("query: done");
      })
      .fail(function(xhr, status, error) {
        console.log("query: fail");
		 //failReturned(xhr.responseText,xhr.status,set,butt);
	 })
      .always(function() {
          
        console.log("query: always");
      });
});
