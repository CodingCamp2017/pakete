<!DOCTYPE html>
<html lang="de">
    <head>
        <title>Post Kundenservice</title>
        
        <?php include('html/head.html'); ?>
    </head>
    
  <body>  
    <?php include('html/navigation.html'); ?>

        <div class="row justify-content-center">
            <div class="col-8">
                <br>
                <div style="display : none" id="info_message_container" class="alert alert-success">info</div>
                <div style="display : none" id="error_message_container" class="alert alert-warning">error</div>
                <!-- Spinning wheel-->
                <div hidden class="mx-auto pageContent" id="spinner">
                    <i class="fa fa-spinner fa-spin" style="font-size:50px" ></i>
                </div>
                
                <h1 class="mt-5">Paketnachverfolgung</h1>                

                <!-- Paket Suche -->
                <div class="mx-auto pageContent" id="update_container">

                <form id="search_id">
                <fieldset>
                  <input type="text" class="form-control" placeholder="ID" id="packet_id" /><br>
                  <input type="submit"  value="Paket suchen" id="update_packet_button" class="btn btn-primary" />
                </fieldset>


                <!-- Paket Metadaten -->
                <form>  
                    <fieldset id="meta_form" disabled hidden>
                        <br>		
                        <div class="container">
                            <div class="row">
                                <div class="col">				
                                    <p>
                                        <b>Absender</b><br>
                                        <input type="text" class="form-control" placeholder="Name" id="sender_name" />
                                        <input type="text" class="form-control" placeholder="Straße" id="sender_street" />            
                                        <input type="text" class="form-control" placeholder="PLZ" id="sender_zip" pattern="[0-9]{5}" />
                                        <input type="text" class="form-control" placeholder="Stadt" id="sender_city" />  
                                    </p>
                                </div>
                                <div class="col">
                                    <p>
                                        <b>Empfänger</b><br>
                                        <input type="text" class="form-control" placeholder="Name" id="receiver_name" />
                                        <input type="text" class="form-control" placeholder="Straße" id="receiver_street" />
                                        <input type="text" class="form-control" placeholder="PLZ" id="receiver_zip" class="zip_input" pattern="[0-9]{5}" />
                                        <input type="text" class="form-control" placeholder="Stadt" id="receiver_city" />
                                    </p>
                                </div>
                                <div class="col">
                                    <p>
                                        <b>Größe</b><br>
                                        <input type="text" class="form-control" id="size" /><br>
                                    </p>
                                    <p>
                                        <b>Gewicht (kg)</b><br>
                                        <input type="text" class="form-control" name="weight" placeholder="10" id="weight" /> <br>
                                    </p>
                                </div>
                            </div>
                        </div>	


                        <!-- Paket Route -->
                        <table id ="Nachverfolgung" class="table table-striped">
                          <thead>
                            <tr>
                              <th>#</th>
                              <th><i class="fa fa-car"></i></th>
                              <th>Ort</th>
                              <th>Datum</th>
                              </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <th scope="row">1</th>
                              <td><i class="fa fa-envelope-o"></i></td>
                              <td id="regloc"></td>
                              <td id="regdate"></td>
                            </tr>
                          </tbody>
                        </table>
                    </fieldset>	
                </form>
	
                <!--Neue Suche-->
            </div>	
          
             <div id="map"></div>	  
            <!-- /.container -->
            </div>
        </div>    

        <?php include('html/scripts.html'); ?>
        <script src="js/tracking.js"></script>
        <script src="js/map.js"></script>
        <!--<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyASQQsfeuEWdnMjDjSKS8HhIjl6Gr6Qzfo&callback=initMap"></script>-->
        <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyASQQsfeuEWdnMjDjSKS8HhIjl6Gr6Qzfo"></script>
  </body>
</html>