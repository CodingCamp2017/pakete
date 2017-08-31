$("#register_button").click(function() {
    register_email = $("#register_email").val();
    register_password = $("#register_password").val();
    
    registerUser(register_email, register_password, function() {
        //success
        infoMessage("Registering user successfully.");
    }, function() {
        //failure
        errorMessage("Error registering user");
    });
});