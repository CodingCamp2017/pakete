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
		$("#weight").val((obj.weight+"").replace('.',","));
		//Liste
		//Erste Spalte
		$("#regloc").text(obj.sender_city);
		$("#regdate").text(obj.packetRegistrationTime);
		//Restliche Spalten
		removeRows();
		
		var arrayLength = obj.stations.length;
		for (var i = 0; i < arrayLength; i++) {
			var row = obj.stations[i];
			addRow(i+2,iconMap(row.vehicle),row.location,row.time);
		}
		//Letzte Spalte
		if(obj.deliveryTime != undefined){
			addRow(i+2,"fa fa-envelope-open-o",obj.receiver_city,obj.deliveryTime);
		}
		serverReturned("",set,butt);
		
      })
      .done(function() {
      })
      .fail(function(xhr, status, error) {
		 failReturned(xhr.responseText,xhr.status,set,butt);
	 })
      .always(cleanUp);
	
	
	
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
function failReturned(error,statu,fset,pbutton){
	console.log( "error " + statu );
	$(fset).prop("disabled", false);
	$(pbutton).prop("hidden",false);
	var errortext = "Ups. Etwas ist schief gegangen. ";
		if(error === undefined){
			errortext +="Der Server reagiert nicht. Überprüfen Sie ihr Internetverbindung und versuchen Sie es später nochmal.";
		}else if(statu == 404){
			
			errortext = "Diese ID exitiert nicht."
			
		}/**else if(statu == 504){
			errortext +="Der Server meldet einen Fehler 504. Versuchen Sie es später nochmal.";
		}*/else{
			errortext += error;
		}
	$("#server_answer").text(errortext);
	}
function cleanUp() {
	$("#server_answer").prop("hidden",false);
	$("#spinner").prop("hidden",true);
}
function iconMap(hash){
		if(hash == "center")return "fa fa-building-o";
		if(hash == "car")return "fa fa-car";
		if(hash == "foot")return "fa fa-bicycle";
		if(hash == "plane")return "fa fa-plane";
		if(hash == "rocket")return "fa fa-rocket";
		if(hash == "ship")return "fa fa-ship";
		if(hash == "train")return "fa fa-subway";
		if(hash == "truck")return "fa fa-truck";
		if(hash == "failed")return "fa fa-frown-o";
		//if(hash == "")return "fa fa-flag-checkered"
}