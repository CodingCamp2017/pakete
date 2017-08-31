var map_url = "https://maps.googleapis.com/maps/api/geocode/json";
var map_api_key = "AIzaSyASQQsfeuEWdnMjDjSKS8HhIjl6Gr6Qzfo";

var map = null;

function address2coords(address) {
    var query = map_url + "?key=" + map_api_key + "&region=de&address=" + address;
    return $.get(query);
}

function zoomToObject(map, obj) {
    var bounds = new google.maps.LatLngBounds();
    var points = obj.getPath().getArray();
    for (var n = 0; n < points.length; n++) {
        bounds.extend(points[n]);
    }
    map.fitBounds(bounds);
}

function showPathInMap(map, stations) {
    console.log("show path in map");
    console.log(stations);

    var requests = stations.map(function (item) {
        return address2coords(item["address"]);
    });

    $.when.apply($, requests).done(function () {
        // Workaround that solves problem that arguments is an array when there are multiple responses,
        // but no array when there is only one response. This makes it an array in every case
        if (stations.length < 2) {
            var responses = [arguments];
        } else {
            var responses = arguments;
        }
        var coords = [];
        var markers = [];
        var infowindows = [];  

        var realIdx = 0;              

        for (var i = 0; i < responses.length; ++i) {            
            if (responses[i][0].status != "OK") {
                console.log(responses[i])
                console.log("Invalid response")                
                continue;
            }            
            
            let idx = realIdx;

            coords[idx] = responses[i][0].results[0].geometry.location;

            markers[idx] = new google.maps.Marker({
                position: coords[idx],
                label: (i + 1).toString(),
                map: map
            });
            
            infowindows[idx] = new google.maps.InfoWindow({
                content: "<i class=\"" + iconMap(stations[i]["vehicle"]) + "\"></i> <b>" + stations[i]["address"] + "</b><br /><b>Zeit:</b> " + stations[i]["time"]
            });            

            markers[idx].addListener('click', function () {
                infowindows[idx].open(map, markers[idx]);
            }); 

            realIdx++;
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
            zoomToObject(map, path);
        } else {
            map.setCenter(coords[0]);
            map.setZoom(8);
        }
    });
}

function initMap() {
    console.log("init map");
    map = new google.maps.Map(document.getElementById('map'));
}