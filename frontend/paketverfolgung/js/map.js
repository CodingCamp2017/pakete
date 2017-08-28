var map = null;

function address2coords(address) {
        return $.get("https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyASQQsfeuEWdnMjDjSKS8HhIjl6Gr6Qzfo&region=de&address=" + address)
      }

      function zoomToObject(map, obj){
        var bounds = new google.maps.LatLngBounds();
        var points = obj.getPath().getArray();
        for (var n = 0; n < points.length ; n++) {
          bounds.extend(points[n]);
        }
        map.fitBounds(bounds);
      }

      function showPathInMap(map, stations) {
      	console.log("show path in map")
      	console.log(stations)        
        var address = encodeURI($("#addr").val())
        
        var requests = stations.map(function(item) { return address2coords(item["address"]) })
        
        $.when.apply($, requests).done(function() {
          // Workaround that solves problem that arguments is an array when there are multiple responses,
          // but no array when there is only one response. This makes it an array in every case
          if (stations.length < 2) {
            var responses = [arguments]
          } else {
            var responses = arguments
          }
          var coords = [];
          var markers = [];
          var infowindows = [];
          
          for (let i = 0; i < responses.length; ++i) {            
            coords[i] = responses[i][0].results[0].geometry.location                      

            markers[i] = new google.maps.Marker({
              position: coords[i],
              label: (i + 1).toString(),
              map: map
            });

            infowindows[i] = new google.maps.InfoWindow({              
              content: "<b>" + stations[i]["address"] + "</b><br /><b>Fahrzeug:</b> <i class=\"" + iconMap(stations[i]["vehicle"]) + "\"></i><br /><b>Zeit:</b> " + stations[i]["time"]
            });

            markers[i].addListener('click', function() {             
              infowindows[i].open(map, markers[i]);
            });
          }          
          
          if (coords.length > 1) {
            var path = new google.maps.Polyline({
            path: coords,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
            });

            path.setMap(map);  
            zoomToObject(map, path)
          } else {            
            map.setCenter(coords[0]);
            map.setZoom(8);
          }
        });
      }

      function initMap() {		 
      	console.log("init map")
        map = new google.maps.Map(document.getElementById('map'));        
      }