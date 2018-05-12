var $j = jQuery.noConflict();
var map;
var locations = [];
var current_location;

function displayEvents(){

}

function populatemarkers() {

    map = new google.maps.Map(document.getElementById('googleMap'), {
        center: new google.maps.LatLng(48.1293954,12.556663),//Setting Initial Position
        zoom: 10
    });
    infoWindow = new google.maps.InfoWindow;
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        current_location = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        infoWindow.setPosition(current_location);
        infoWindow.setContent('You are here!');
        infoWindow.open(map);
        map.setCenter(current_location);

        var lat = document.getElementById("lat-input");
        console.log(current_location.lat);
        lat.value = current_location.lat;

        var lng = document.getElementById("lng-input");
        console.log(current_location.lng);
        lng.value = current_location.lng;
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }

    // add search box in the map
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
      var places = searchBox.getPlaces();
      if (places.length == 0) {
        return;
      }
      if (places.length == 1) {
        var place = places[0];
        var location = document.getElementById("loc-input");
        console.log(place.name);
        location.value = place.name;

        var lat = document.getElementById("lat-input");
        console.log(place.geometry.location.lat());
        lat.value = place.geometry.location.lat();

        var lng = document.getElementById("lng-input");
        console.log(place.geometry.location.lng());
        lng.value = place.geometry.location.lng();
      }

      // Clear out the old markers.
      markers.forEach(function(marker) {
        marker.setMap(null);
      });
      markers = [];

      // For each place, get the icon, name and location.
      var bounds = new google.maps.LatLngBounds();
      places.forEach(function(place) {
        if (!place.geometry) {
          console.log("Returned place contains no geometry");
          return;
        }
        // var icon = {
        //   url: "http://weclipart.com/gimg/6B088DE2AFDC55FB/google-maps.svg",
        //   size: new google.maps.Size(71, 60),
        //   origin: new google.maps.Point(0, 0),
        //   anchor: new google.maps.Point(17, 34),
        //   scaledSize: new google.maps.Size(25, 25)
        // };

        // Create a marker for each place.
        markers.push(new google.maps.Marker({
          map: map,
          // icon: icon,
          label: "O",
          // color: blue,
          title: place.name,
          position: place.geometry.location
        }));

        // marker.click

        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      map.fitBounds(bounds);
    });

    
    $j.get("/hypermap/get_items")
    .done(function(data) {
        console.log("populatemarkers is running.");
        // add posts
        
        for (var i = 0; i < data.items.length; i++) {
            item = data.items[i];
            console.log(item);
            var markerLat = item['lat'];
            var markerLng = item['lng'];
            var newLoc = {lat: markerLat, lng: markerLng};
            locations.push(newLoc);
            console.log(newLoc);
            var newMarker = new google.maps.Marker({
              position: newLoc,
              map: map,
              animation: google.maps.Animation.DROP,
            });
            markers.push(newMarker);
            addTrigger(newMarker, item['id']);
            console.log(item['id']);
            // var id = item['id'];
            // newMarker.addListener('click', function(){showEvents(id)});
            if(i == (data.items.length - 1)) {
              console.log(newLoc);
              map.panTo(newLoc);}
        }
        var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
        map.setZoom(15);
        
        console.log("populatemarkers done.");
        // popolate_done = true
      }).fail(function() {
      console.log("Failed to populatemarkers.");
    });
}

function addTrigger(marker, id){
    marker.addListener('click', function(){showEvents(id)});
}

function showEvents(id){
    console.log("showing CE." + id);
    // var latitude = marker.getPosition().lat();
    // var longitude = marker.getPosition().lng();
    $j.get("/hypermap/get-ce/"+id)
    .done(function(data) {
        console.log("showing_event" +id);
        var event = $j("#current-event");
        event.replaceWith(data.eventhtml);
        // var html = data["eventhtml"];
        // console.log(data.eventhtml);
        // event.append(data.eventhtml);
        $j("#like-btn").on("click", function(e) { 
          e.preventDefault();
          var button = $j(this);
           // onclick=\"location.href='{% url 'like' item.id %}'\"
          $j.get("/hypermap/like/" + id).done(function(data) {
            if (data.liked) {
              button.text("Unlike(" + data.count + ")");
            } else {
              button.text("Like(" + data.count + ")");
            }
          });
        });
    });
}

$j(document).ready(function ()
{
    loadScript();
});


function loadScript() {
      var script = document.createElement('script');
      // script.type = 'text/javascript';
      script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBelEVCZyRl-yf72Hnex47q2eZo9rtUJNk&libraries=places&callback=populatemarkers";
      document.body.appendChild(script);
      // var script1 = document.createElement('script');
      // script1.src = "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js";
      // document.body.appendChild(script1);
}