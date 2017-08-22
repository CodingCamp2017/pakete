$(function() {
  var server_url = "http://localhost:5000/";

 //Send Location update
  $("#update_form").submit(function() {
    var data = {"packet_id" : $("#packet_id").val() } 
	console.log( data);
	var set = "#update_form fieldset";
	var butt = "#update_packet_button";
    var jqxhr = $.post( server_url, data, function(value) {
      serverReturnd(value,set,butt);
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