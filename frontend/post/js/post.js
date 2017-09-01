$(function() {
  var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000/";

  $("#register_link").click(function() {
	  removeAll();
   $("#register_container").show();
    $("#register_link_container").addClass("active");
  });

  $("#update_link").click(function() {
	  removeAll();
    $("#update_container").show();
    $("#update_link_container").addClass("active");
  });
  
  function removeAll(){
	$("#register_container").hide();
    $("#register_link_container").removeClass("active"); 
	$("#update_container").hide();
    $("#update_link_container").removeClass("active");
  }

  $("#is_delivered").click(function() {
    if ($("#is_delivered").prop("checked")) {           
      $("#station_container").hide()
    } else {
      $("#station_container").show()
    }
  });
	
  //Send registation
  $("#register_form").submit(function() {
	  //Does User exist?
	
	
	if($("#email").val().length!==0){
		//TODO
		showError("email");
		errorMessage("Diese Email hat keinen Account. Erstellen sie einen Account auf der Paketverfolgungsseite.")
		$("#server_answer").prop("hidden",false);
		$("#server_answer").text("Diese Email hat keinen Account. Erstellen sie einen Account auf der Paketverfolgungsseite.");
		return false;
	}else{
		$("#email").removeClass("error");
	}
	
    var data = {"sender_name" :     $("#sender_name").val(),
				"sender_street" :   $("#sender_street").val(),
                "sender_zip" :      $("#sender_zip").val(),
                "sender_city" :     $("#sender_city").val(),
				"receiver_name" :   $("#receiver_name").val(),
                "receiver_street" : $("#receiver_street").val(),
                "receiver_zip" :    $("#receiver_zip").val(),
                "receiver_city" :   $("#receiver_city").val(),
                "size" :            $('input[name=size]:checked').val(),
                "weight" :          $("#weight").val().replace(',',"."),
				'auto_deliver':		$('#auto_deliver').prop("checked")
                }
		console.log(data);
      var set = "#register_form fieldset";
      var butt = "#register_packet_button";
      var jqxhr = $.post(server_url + "register", data, function(obj) {
		  console.log(obj);
		serverReturned("Ihr Paket wurde registriert. Es hat die ID " + obj.packet_id,set,butt);
		$("#qrcode").prop("src","https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + obj.packet_id);
		//TODO send id an Nutzerkonto
      })
      //.done(function() {
      //})
      .fail(function(xhr, status, error) {
		 failReturned(xhr.responseText,xhr.status,set,butt);
		
	    })
      .always(cleanUp);
	  
	    waitOnServer(set,butt);
      return false;
  });
 
 //Send Location update
  $("#update_form").submit(function() {
	if($("#packet_id").val().length ===0){
		return false;
	}
    var data = {"packet_id" : $("#packet_id").val() } 
	adresse = server_url+'packet/'+$("#packet_id").val();
	if(!$("#is_delivered").prop("checked")){
		data.station = $("#station").val();
		data.vehicle = $('input[name=vehicle]:checked').val();
		adresse += "/update";
	} else {
    adresse += "/delivered";    
  }
	console.log( data);
	console.log(adresse)
	var set = "#update_form fieldset";
	var butt = "#update_packet_button";
    var jqxhr = $.post( adresse, data, function() {
      serverReturned("Verbleib des Pakets wurde aktualisiert.",set,butt);
      })
      //.done(function() {
      //})
      .fail(function(xhr, status, error) {
		  
        failReturned(xhr.responseText,xhr.status,set,butt);
	    })
      .always(cleanUp);
	waitOnServer(set,butt);
    return false;
  });
  
});

//Sichtbarkeit ändern
function waitOnServer(fset,pbutton){
	$(fset).prop("disabled", true);
	$(pbutton).prop("hidden",true);
	$("#spinner").prop("hidden",false);
    $('#info_message_container').hide();	
    $('#error_message_container').hide();
}
function serverReturned(info,fset,pbutton){
	console.log("Request successful");
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	if(info !== undefined && info.length > 0) {
        infoMessage(info);
    }	
}

function failReturned(responseText,statu,fset,pbutton){
	console.log( "error " + statu);
	
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	var errortext = "Ups. Etwas ist schief gegangen. ";
		if(responseText === undefined){
			//0 no conection
			errortext +="Der Server reagiert nicht. Überprüfen Sie ihr Internetverbindung und versuchen Sie es später nochmal.";
		}else if(statu == 400 || statu == 404){
			var obj = JSON.parse(responseText);
			if(obj.type == "invalid key"){
				showError(obj.key);
				errortext = "Eine Eingabe ist nicht richtig.";
			}else {
				errortext += "Server meldet: " + obj.message;
			}
			console.log(obj.message);
		}else if(statu == 504){
			errortext +="Der Server meldet einen Fehler 504. Versuchen Sie es später nochmal.";
		}else{
			errortext += error;
		}
	errorMessage(errortext);
	}
function cleanUp() {
	
	$("#spinner").prop("hidden",true);
	//console.log( "finished" );
}
function showError(string){
	string = "#"+string;
	$(string).addClass("error");
	$(string).keydown(function(){
		$(string).removeClass("error");
		$(string).off("keydown");
	});
}


function errorMessage(message) {
    $('#info_message_container').hide();
    $('#error_message_container').html(message).show();    
}

function infoMessage(message) {
    $('#error_message_container').hide();
    $('#info_message_container').html(message).show();
}



