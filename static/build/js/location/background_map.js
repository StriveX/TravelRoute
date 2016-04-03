var map;

function showGoogleMaps() {

    var mapOptions = {
        zoom: 12, // initialize zoom level - the max value is 21
        streetViewControl: false, // hide the yellow Street View pegman
        scaleControl: true, // allow users to zoom the Google Map
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: {lat: 37.7749295, lng: -122.41941550000001},
    };

    map = new google.maps.Map(document.getElementById('background_map'),
        mapOptions);

    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        map.setCenter(pos);
    }, function() {

    });
  }
}

google.maps.event.addDomListener(window, 'load', showGoogleMaps);