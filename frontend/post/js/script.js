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

  $("#register_form").submit(function() {
    var data = {"sender_street" :   $("#sender_street").val(),
                "sender_zip" :      $("#sender_zip").val(),
                "sender_city" :     $("#sender_city").val(),
                "receiver_street" : $("#receiver_street").val(),
                "receiver_zip" :    $("#receiver_zip").val(),
                "receiver_city" :   $("#receiver_city").val(),
                "weight" :          $("#weight").val()
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

    return false;
  });

  $("#update_form").submit(function() {
    console.log("update form submit")
    return false;
  })
});