$(function() {
  var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/";

 //Send Location update
  $("#update_form").submit(function() {
	  
   // var data = {"id" : $("#packet_id").val() } 
	var set = "#packet_id";
	var butt = "#update_packet_button";
	waitOnServer(set,butt);
	var jqxhr = $.get( server_url + "packetStatus/"+$("#packet_id").val(), function(responseText) {
		
			var obj = JSON.parse(responseText);
			//sender Adresse
			$("#sender_name").val(obj.sender_name);
			$("#sender_street").val(obj.sender_street);
			$("#sender_city").val(obj.sender_city);
			$("#sender_zip").val(obj.sender_zip);
			//reciver Adresse
			$("#receiver_name").val(obj.receiver_name);
			$("#receiver_street").val(obj.receiver_street);
			$("#receiver_city").val(obj.receiver_city);
			$("#receiver_zip").val(obj.receiver_zip);
			
			$("#size").val(obj.size);
			$("#weight").val(obj.weight);
			serverReturned(responseText,set,butt);
	
		
      })
      .done(function() {
        console.log( "second success" );
      })
      .fail(function() {
		 failReturned(set,butt);
	 })
      .always(cleanUp);
	
	removeRows();
	addRow(1,"fa fa-bicycle","BKA","30.Febuar");
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
	$("#meta_form").prop("hidden",true);
}
function serverReturned(info,fset,pbutton){
	console.log("Request successful");
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	$("#server_answer").text(info);
	$("#meta_form").prop("hidden",false);
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