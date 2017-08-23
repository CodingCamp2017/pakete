$(function() {
  var server_url = "http://localhost:5000/";

 //Send Location update
  $("#update_form").submit(function() {
    var data = {"id" : $("#packet_id").val() } 
	console.log( data);
	var set = "#update_form fieldset";
	var butt = "#update_packet_button";
    var jqxhr = $.post( server_url, data, function(value) {
      serverReturned(value,set,butt);
      })
      .done(function() {
        console.log( "second success" );
      })
      .fail(function() {
		 failReturned(set,butt);
	  })
      .always(cleanUp);
	waitOnServer(set,butt);
	removeRows();
	setTimeout(function() {
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
	},100);
	return false;
  });
  
});
//int/String/String/String
function addRow(index,symbol,loca,date){
	$('#Nachverfolgung > tbody:last-child').append('<tr name="addedRow"><th scope="row">'+index+'</th><td><i class="'+symbol+'"></i></td><td>'+loca+'</td><td>'+date+'</td></tr>');
    
}
function removeRows(){
	$("[name='addedRow']").remove();
}
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

function failReturned(fset,pbutton){
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