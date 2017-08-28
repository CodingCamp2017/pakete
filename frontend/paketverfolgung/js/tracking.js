		
$(function() {
  var server_url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/";
  var stations = [{"vehicle" : "envelope", "address" : "????", "time" : getDate("0") }];;
  var set = "#packet_id";
  var butt = "#update_packet_button";
 // var socket = io.connect('http://localhost:8001/packetStatus');//http://localhost:8001/
  var socket = io.connect('http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001/packetStatus');//http://localhost:8001/
  var id;
  var ids= new Set();
 //Send Location update
  $("#update_form").submit(function() {
    initMap()
	waitOnServer(set,butt);
	id = $("#packet_id").val();
	$.get( server_url + "packetStatus/"+id, function(responseText) {
		
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
		$("#regdate").text(getDate(obj.packetRegistrationTime));
		//Restliche Spalten
		removeRows();

		// TODO whole address, not only city
		stations = [{"vehicle" : "envelope", "address" : getAbsender(), "time" : getDate(obj.packetRegistrationTime) }];

		var arrayLength = obj.stations.length;
		for (var i = 0; i < arrayLength; i++) {
			var row = obj.stations[i];			
			addRow(row.vehicle,row.location,row.time);
		}
		//Letzte Spalte
		if(obj.deliveryTime != undefined){
			addRow("envelope-o",obj.receiver_city,obj.deliveryTime,getReciver());	
		}
		serverReturned("",set,butt);
		showPathInMap(map, stations);
		if(!ids.has(id)){
			ids.add(id);
			socket.emit('subscribe', {packet_id: id});
		}	
      })
      .done(function() {
      })
      .fail(function(xhr, status, error) {
		 failReturned(xhr.responseText,xhr.status,set,butt);
	 })
      .always(cleanUp);
	return false;
  });
  //Socket
  
    socket.on('update', function(obj){
		console.log(id);
		console.log(obj)
		if(id != undefined && obj.packet_id != undefined && obj.packet_id != id){
			serverReturned("Das Paket mit der ID " + obj.packet_id + " wurde an einen neuen Standort registriert.",set,butt);
			return;
		}
	  if(obj.location === undefined){
			addRow("envelope-o",$("#receiver_city").val(),obj.deliveryTime,getReciver());
			serverReturned("Ihr Paket ist da, schauen Sie in ihren Briefkasten.",set,butt);
	  }else{
		   addRow(obj.vehicle,obj.location,obj.time);
			serverReturned("Ihr Paket wurde soeben in "+obj.location+" gemeldet!",set,butt);
	  
	  }
	  showPathInMap(map, stations);
	});
	  
  //int/String/String/String
	function addRow(symbol,loca,date,address){
		var date = getDate(date);
		if(address === undefined)address = loca;
		stations.push({"vehicle" : symbol, "address" : address, "time" : date })
		$('#Nachverfolgung > tbody:last-child').append('<tr name="addedRow"><th scope="row">'+stations.length+'</th><td><i class="'+iconMap(symbol)+'"></i></td><td>'+loca+'</td><td>'+date+'</td></tr>');
	}
	function removeRows(){
		$("[name='addedRow']").remove();
	}
  //Login
  $("#login").click(function(){
    login_email = $("#email").val();
    login_password = $("#password").val();
        
    loginUser(login_email, login_password, function() {
        //login succsess       
        console.log("Logging in user successfully.");
	$("#login_bar").prop("hidden",true);
	$("#eingeloggt_bar").prop("hidden",false);
        $("#email_label").html(login_email);
    }, function() {
        //failure
        console.log("Error authenticating user");
    });
    return false;
  });
  //Logout
  $("#logout").click(function(){
	  //try to logout
	  
	  //logout succsess
	  $("#login_bar").prop("hidden",false);
	  $("#eingeloggt_bar").prop("hidden",true);
	  return false;
  });
});

function getDate(date){
	if(date.toString().includes("/")){
		return date;
	}else{
		var date = new Date(parseInt(date)*1000);
		var text = "";
		var x = date.getDate();
		if(x < 10){
			text += "0"
		}
		text += x + ".";
		x = date.getMonth()+1;
		if(x < 10){
			text += "0"
		}
		text += x + "."+date.getFullYear()  + " ";
		x = date.getHours();
		if(x < 10){
			text += "0"
		}
		text += x + ":";
			x = date.getMinutes();
		if(x < 10){
			text += "0"
		}
		text += x;
		return text;
	}
	return false;
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
		if(hash == "envelope")return "fa fa-envelope-o";
		if(hash == "envelope-o")return "fa fa-envelope-open-o";
		if(hash == "center")return "fa fa-building-o";
		if(hash == "car")return "fa fa-car";
		if(hash == "foot")return "fa fa-bicycle";
		if(hash == "plane")return "fa fa-plane";
		if(hash == "rocket")return "fa fa-rocket";
		if(hash == "ship")return "fa fa-ship";
		if(hash == "train")return "fa fa-subway";
		if(hash == "truck")return "fa fa-truck";
		if(hash == "failed")return "fa fa-frown-o";		
}
function getAbsender(){
	return $("#sender_zip").val()+ " " +$("#sender_city").val() + ", " + " "+$("#sender_street").val();
}
function getReciver(){
	return $("#receiver_zip").val()+ " " +$("#receiver_city").val() + ", " + " "+$("#receiver_street").val();
}