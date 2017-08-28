<!DOCTYPE html>
<html lang="de">
    <head>
        <title>Benutzer registrieren - Post Kundenservice</title>
        <?php include('html/head.html'); ?>
        <script src="js/user_info.js"></script>
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
    <?php include('html/scripts.html'); ?>
  </body>
</html>