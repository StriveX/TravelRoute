var map;
var iconPath = '../static/build/images/';

function loadPlaces(map) {
    var bounds = map.getBounds();
    $.ajax({
        url : "api/",
        type : "GET",
        data: {bounds: bounds},
        success : function(json) {
            $.each(json, function(i, val) {
                var position = {lat: Number(val.latitude), lng: Number(val.longitude)};
                console.log(position);
                var marker = new google.maps.Marker({
                    map: map,
                    position: position,
                    icon: iconPath + 'map_marker.png'
                });
            });
        },
        error : function(xhr,errmsg,err) {

        }
    });
}

function showGoogleMaps() {

    var mapOptions = {
        zoom: 12, // initialize zoom level - the max value is 21
        streetViewControl: false, // hide the yellow Street View pegman
        scaleControl: true, // allow users to zoom the Google Map
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: {lat: 37.7749295, lng: -122.41941550000001}
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
        });
    }

    loadPlaces(map);
    google.maps.event.addListener(map, 'idle', function(ev){

    });
}

google.maps.event.addDomListener(window, 'load', showGoogleMaps);
