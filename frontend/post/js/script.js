$(function() {
	
  $("#register_link").click(function() {
    $("#update_container").hide();
    $("#update_link_container").removeClass("active");
    $("#register_container").show();
    $("#register_link_container").addClass("active");
  });

  $("#update_link").click(function() {
    $("#update_container").show();
    $("#update_link_container").addClass("active");
    $("#register_container").hide();
    $("#register_link_container").removeClass("active");
  });

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
                "weight" :          $("#weight").val()
                }

    console.log(data);
	var set = "#register_form fieldset";
	var butt = "#register_packet_button";
    var jqxhr = $.post( "http://localhost:8000", JSON.stringify(data), function(result) {
		serverReturnd("Ihr Paket wurde registrieren. Es hat die ID #######",set,butt);		
      }, "json")
      .done(function() {
        console.log( "second success" );
      })
      .fail(function() {
		failReturnd(set,butt);
	  })
      .always(cleanUp);
	  
	waitOnServer(set,butt);
    return false;
  });
 //Send Location update
  $("#update_form").submit(function() {
    var data = {"packet_id" :   $("#packet_id").val()         
                }
	var adresse = "http://localhost:8000";
	if(!$("#is_delivered").prop("checked")){
		data.station = $("#station").val();
		adresse = "http://localhost:8000";
	}
    console.log(data);
	var set = "#update_form fieldset";
	var butt = "#update_packet_button";
    var jqxhr = $.post( adresse, data, function() {
      serverReturnd("Verbleib des Pakets wurde aktualisiert.",set,butt);
      })
      .done(function() {
        console.log( "second success" );
      })
      .fail(function() {
		failReturnd(set,butt);
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
function serverReturnd(info,fset,pbutton){
	console.log("Request successful");
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	$("#server_answer").text(info);		
}

function failReturnd(fset,pbutton){
	console.log( "error" );
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	$("#server_answer").text("Ups. Etwas ist schief gegangen. Überprüfen sie ihre Internetverbindung und versuchens sie es nochmal.");	
}
function cleanUp() {
	$("#server_answer").prop("hidden",false);
	$("#spinner").prop("hidden",true);
	console.log( "finished" );
}