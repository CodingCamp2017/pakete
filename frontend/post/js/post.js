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
    var data = {"sender_name" :     $("#sender_name").val(),
				"sender_street" :   $("#sender_street").val(),
                "sender_zip" :      $("#sender_zip").val(),
                "sender_city" :     $("#sender_city").val(),
				"receiver_name" :   $("#receiver_name").val(),
                "receiver_street" : $("#receiver_street").val(),
                "receiver_zip" :    $("#receiver_zip").val(),
                "receiver_city" :   $("#receiver_city").val(),
                "size" :            $('input[name=size]:checked').val(),
                "weight" :          $("#weight").val().replace(',',".")
                }

      var set = "#register_form fieldset";
      var butt = "#register_packet_button";
      var jqxhr = $.post(server_url + "register", data, function(obj) {
		  console.log(obj);
		serverReturned("Ihr Paket wurde registriert. Es hat die ID " + obj.id,set,butt);
		$("#qrcode").prop("src","https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + obj.id);
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
	$("#server_answer").prop("hidden",true);
}
function serverReturned(info,fset,pbutton){
	console.log("Request successful");
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	$("#server_answer").text(info);		
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
				errortext = "Ein Input ist nicht richtig.";
			}else {
				errortext += "Server meldet: " + data.message;
			}
			console.log(obj.message);
		}else if(statu == 504){
			errortext +="Der Server meldet einen Fehler 504. Versuchen Sie es später nochmal.";
		}else{
			errortext += error;
		}
	$("#server_answer").text(errortext);
	}
function cleanUp() {
	$("#server_answer").prop("hidden",false);
	$("#spinner").prop("hidden",true);
	//console.log( "finished" );
}
function showError(string){
	string = "#"+string;
	$(string).addClass("error");
	$(string).keypress(function(){
		$(string).removeClass("error");
		$(string).off("keypress");
	});
	prev = string;
}