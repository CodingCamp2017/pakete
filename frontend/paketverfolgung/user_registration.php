<!DOCTYPE html>
<html lang="de">
    <head>
        <title>Benutzer registrieren - Post Kundenservice</title>
        <?php include('html/head.html'); ?>

    </head>  
    <body>
        <?php include('html/navigation.html'); ?>

        <div class="row justify-content-center">
            <div class="col-8">
                <div class="mx-auto pageContent">
                    <br>
                    <div id="info_message_container" class="alert alert-success">info</div>
                    <div id="error_message_container" class="alert alert-warning">error</div>
                    <!-- Spinning wheel-->
                    <div class="mx-auto pageContent" >
                        <i hidden class="fa fa-spinner fa-spin" style="font-size:50px" id="spinner"></i><br/>
                    </div>
                    
                    <h1>Neuen Benutzer registrieren</h1>

                    <form id="register_form">
                        <input type="text" class="form-control" placeholder="Email" id="register_email" /><br>
                        <input type="password" class="form-control" placeholder="Choose a password" id="register_password" /><br>
                        <input type="button" value="Registrieren" id="register_button" class="btn btn-primary" />
                    </form>
                </div>
            </div>
        </div>
        <?php include('html/scripts.html'); ?>
        <script src="js/user_registration.js"></script>
  </body>
</html>