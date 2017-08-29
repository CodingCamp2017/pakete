<!DOCTYPE html>
<html lang="de">
    <head>
        <title>Benutzer registrieren - Post Kundenservice</title>
        <?php include('html/head.html'); ?>
        
        <script>
            function requestSession() {
                // send request and store session id in coockie
                var query = "http://localhost:8002/request_session";
                
                console.log("query: " + query);

                $.post(query, function(data) {
                    console.log("query done: " + data);
                    writeSessioIdCookie(data);
                  });
            }
            
            function sendSession() {
                var query = "http://localhost:8002/send_session";

                var requestData = {};
                
                var sessionId = readSessionIdCookie();
                if(sessionId !== undefined) {
                    requestData = {"session_id": sessionId};
                } else {
                    console.log("no session id available");
                }
    
                // send request including session id to server
                $.post(query, requestData, function(data) {
                    console.log("query done: " + data); 
                  });
            }
            
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
        </script>
</head>
    <body>
        <?php include('html/navigation.html'); ?>

    <div class="row justify-content-center">
        <div class="col-8">
            <div class="mx-auto pageContent">
                <a class="btn btn-primary" onclick="requestSession();">Request session</a><br>    
                <a class="btn btn-primary" onclick="sendSession();">Send session</a><br>       
                <a class="btn btn-primary" onclick="readCookies();">Read cookies</a><br>          
            </div>
        </div>
    </div>  
        
    <script src="vendor/jquery/jquery.min.js"></script>
    <script src="vendor/popper/popper.min.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.min.js"></script>

    <script src="js/user_management.js"></script>

    <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">    
    <link href="css/style.css" rel="stylesheet">
     <!-- rotating Waits CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>

  </body>
</html>