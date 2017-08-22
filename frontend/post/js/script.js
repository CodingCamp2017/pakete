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

    var jqxhr = $.post( "http://localhost:8000", data, function(result) {
      console.log("Request successful")
		$("#server_answer").text("Ihr Paket wurde registrieren. Es hat die ID #######");
		$("#next_packet_button").prop("hidden",false);
		
      })
      .done(function() {
        console.log( "second success" );
      })
      .fail(function() {
        console.log( "error" );
		//$("#server_answer").text("Ups. Etwas ist schief gegangen. Überprüfen sie ihre Internetverbindung und versuchens sie es nochmal.")
		//$("#register_form fieldset").prop("disabled", false);
		//$("#register_packet_button").prop("hidden",false);
		$("#server_answer").text("Ihr Paket wurde registrieren. Es hat die ID #######");
		$("#next_packet_button").prop("hidden",false);
		
      })
      .always(function() {
		$("#server_answer").prop("hidden",false);
		$("#spinner").prop("hidden",true);
        console.log( "finished" );
      });
	  
	$("#register_form fieldset").prop("disabled", true);
	$("#register_packet_button").prop("hidden",true);
	$("#spinner").prop("hidden",false);
	$("#server_answer").prop("hidden",true);
    return false;
  });
 //Send Location update
  $("#update_packet_button").submit(function() {
    var data = {"packet_id" :   $("#packet_id").val(),
                "is_delivered" :$("#is_delivered").val(),
                "station" :     $("#station").val()
                }

    console.log(data);

    var jqxhr = $.post( "http://localhost:8000", data, function() {
      console.log("Request successful")
      })
      .done(function() {
        console.log( "second success" );
      })
      .fail(function() {
        console.log( "error" );
      })
      .always(function() {
        console.log( "finished" );
      });
  });
  $("#update_form").submit(function() {
    console.log("update form submit")
    return false;
  });
  //allwo a second packge to be send
  $("#next_packet_button").click(function() {
    $("#next_packet_button").prop("hidden",true);
	$("#register_form fieldset").prop("disabled", false);
	$("#register_packet_button").prop("hidden",false);
	$("#server_answer").prop("hidden",true);
	return false;
  });
});