$(function() {
    setLoginbarStatus();
    $('#info_message_container').hide();
    $('#error_message_container').hide();
});

function errorMessage(message) {
    $('#info_message_container').hide();
    $('#error_message_container').html(message).show();    
}

function infoMessage(message) {
    $('#error_message_container').hide();
    $('#info_message_container').html(message).show();
}

function clearMessage() {
    $('#info_message_container').hide();
    $('#error_message_container').hide();
}

function setLoginbarStatus() {
    // shows login promt if no user logged in, else user mail adress
    if(userLoggedIn()) {
        $("#login_bar").prop("hidden", true);
        $("#eingeloggt_bar").prop("hidden", false);
        $("#email_label").html(readEmailCookie()); // TODO insert mail adress
    } else {
        $("#login_bar").prop("hidden", false);
        $("#eingeloggt_bar").prop("hidden", true);
    }
}

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

$("#button_logout_user").click(function () {
    logoutUser(function () {
        //success
        setLoginbarStatus();
        infoMessage("Logout successfull.");
        
        if(!location.pathname.endsWith("index.php")) {
            // redirect to index after 1 second
            setTimeout(function () {
                location = "index.php";
            }, 1000); 
        }
    }, function (message) {
        // failure
        errorMessage(message);
    });
});

$("#button_login_user").click(function () {
    var login_email = $("#email").val();
    var login_password = $("#password").val();

    loginUser(login_email, login_password, function () {
        //succsess       
        setLoginbarStatus();
        infoMessage("Login successfull.");
    }, function (message) {
        //failure
        errorMessage(message);
    });
    return false;
});