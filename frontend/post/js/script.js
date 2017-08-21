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

  $("#register_packet_button").click(function() {
    var data = {"sender_street" :   $("#sender_street").val(),
                "sender_zip" :      $("#sender_zip").val(),
                "sender_city" :     $("#sender_city").val(),
                "receiver_street" : $("#receiver_street").val(),
                "receiver_zip" :    $("#receiver_zip").val(),
                "receiver_city" :   $("#receiver_city").val(),
                "weight" :          $("#weight").val()
                }

    console.log(data);
  });
});