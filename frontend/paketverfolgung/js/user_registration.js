$("#register_button").click(function() {
    register_email = $("#register_email").val();
    register_password = $("#register_password").val();
    
    if(!register_email || !register_password || register_email.length === 0 || register_password.length === 0) {
        errorMessage("Email or password not provided.");
        return;
    }
    
    registerUser(register_email, register_password, function() {
        //success
        infoMessage("Registering user successfully.");
    }, function() {
        //failure
        errorMessage("Error registering user");
    });
});