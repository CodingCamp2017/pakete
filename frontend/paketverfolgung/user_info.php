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
                <br><br>
                <h1>User Info</h1>
                <br>
                <h2>Pakete</h2>

                <table id ="table_user_packets" class="table table-striped">
                  <thead>
                      <tr>
                          <th>#</th>
                          <th>Paket</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr>
                          <th scope="row">1</th>
                          <td>paketname</td>
                      </tr>
                  </tbody>
                </table>
                
                <br>
                  <h2>Pakte hinzufügen</h2>               
                    <input type="text" class="form-control" placeholder="Paket ID" id="add_packet_id" /><br>
                    <input type="submit"  value="Paket hinzufügen" id="add_packet_button" class="btn btn-primary" />
                  
                <br>
                <br>
                <h2>Account entfernen</h2>
                  <input type='button' value='User löschen' class='btn btn-primary' id ='button_delete_user' />

                  <!--bestätigung ID-->
                  <div class="mx-auto pageContent" >
                  <i hidden class="fa fa-spinner fa-spin" style="font-size:50px" id="spinner"></i><br/>
                      <div hidden id="server_answer"></div>
                  </div>                 
            </div>
        </div>
    </div>  
        
    <script src="vendor/jquery/jquery.min.js"></script>
<script src="vendor/popper/popper.min.js"></script>
<script src="vendor/bootstrap/js/bootstrap.min.js"></script>

<script src="js/user_management.js"></script>

<!--<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyASQQsfeuEWdnMjDjSKS8HhIjl6Gr6Qzfo&callback=initMap"></script>-->
<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyASQQsfeuEWdnMjDjSKS8HhIjl6Gr6Qzfo"></script>

<link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">    
<link href="css/style.css" rel="stylesheet">
 <!-- rotating Waits CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>


    <script src="js/user_info.js"></script>
  </body>
</html>