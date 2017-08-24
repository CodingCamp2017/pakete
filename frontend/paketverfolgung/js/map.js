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

      function showPathInMap(map, addresses) {
      	console.log("show path in map")
      	console.log(addresses)
        var address = encodeURI($("#addr").val())
        
        var requests = addresses.map(function(item) { return address2coords(item) })
        
        $.when.apply($, requests).done(function() {
          var responses = arguments
          var coords = [];
          var markers = [];
          var infowindows = [];

          // TODO map this shit
          for (let i = 0; i < responses.length; ++i) {
            coords[i] = responses[i][0].results[0].geometry.location                      

            markers[i] = new google.maps.Marker({
              position: coords[i],
              label: (i + 1).toString(),
              map: map
            });

            infowindows[i] = new google.maps.InfoWindow({              
              content: "<b>" + addresses[i] + "</b><br />Hier kommen weitere Infos wie Uhrzeit, type"
            });

            markers[i].addListener('click', function() {             
              infowindows[i].open(map, markers[i]);
            });
          }          

          var path = new google.maps.Polyline({
            path: coords,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
          });

          path.setMap(map);
          zoomToObject(map, path)
        });
      }

      function initMap() {
		 
      	console.log("init map")
        map = new google.maps.Map(document.getElementById('map'));  
			
      }