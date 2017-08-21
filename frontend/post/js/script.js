$(function() {        
  $("#is_delivered").click(function() {
    if ($("#is_delivered").prop("checked")) {           
      $("#station_container").hide()
    } else {
      $("#station_container").show()
    }
  });

  $("#register_link").click(function() {
    $("#update_container").hide();
    $("#register_container").show();
  });

  $("#update_link").click(function() {
    $("#update_container").show();
    $("#register_container").hide();
  });
});