function writeSessioIdCookie(serverResponseJson) {
    if("session_id" in serverResponseJson) {
        var sessionId = serverResponseJson['session_id'];
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

function clearSessionIdCookie() {
    document.cookie = "session_id=;";
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
            var s = c.substring(name.length, c.length);
            if(s.length === 0) {
                return undefined;
            } 
            return s;
        }
    }

    return undefined;
}

function userLoggedIn() {
    return !(readSessionIdCookie() === undefined);
}