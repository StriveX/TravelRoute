var map;
var route;
var markers = [];                         // all general markers
var focused_markers = [];                 // unselected_marker showing info window, only one allowed
var selected_markers = [];                // markers in one route
var iconBase = '../static/build/images/';

function addMark(p_id, position, icon, group) {
    var marker = new google.maps.Marker({
        map: map,
        p_id: p_id,
        position: position,
        icon: iconBase + icon
    });
    group.push(marker);
    return marker
}

function add_place_to_route() {

}

function loadPlaces() {
    var bounds = map.getBounds();
    console.log(bounds);
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    $.ajax({
        url : "load_places?n=" + ne.lat() + "&e=" + ne.lng() + "&s=" + sw.lat() + "&w=" + sw.lng(),
        type : "GET",
        success : function(json) {
            $.each(json, function(i, val) {
                var latlng = val.latlng;
                var position = {lat: latlng[0], lng: latlng[1]};

                var marker = new google.maps.Marker({
                    map: map,
                    p_id: val.id,
                    position: position,
                    icon: iconBase + 'Marker_balck.png'
                });
                markers.push(marker);

                google.maps.event.addListener(markers, "click", function (e) {

                });
            });
        },
        error : function(xhr,errmsg,err) {
        }
    });
}

function showGoogleMaps() {

    var input = document.getElementById('search-box');
    var searchBox = new google.maps.places.SearchBox(input);


    var mapOptions = {
        zoom: 12, // initialize zoom level - the max value is 21
        streetViewControl: false,
        scaleControl: true, // allow users to zoom the Google Map
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: {lat: 37.7749295, lng: -122.41941550000001},
        mapTypeControl: false,
        scrollwheel: false
    };

    map = new google.maps.Map(document.getElementById('background_map'),
        mapOptions);
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(input);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
        });
    }

    map.enableKeyDragZoom({
        paneStyle: {
          backgroundColor: "gray",
          opacity: 0.2
        }
    });
    var dz = map.getDragZoomObject();
    google.maps.event.addListener(dz, 'dragstart', function() {
           // do things
    });
    google.maps.event.addListener(dz, 'dragend', function(bnds) {
        console.log(bnds);
        for (var i=0; i < markers.length; i++)
        {
            if (bnds.contains(markers[i].getPosition()))
            {
                var selected_marker = markers[i];
                selected_markers.push(selected_marker);
            }
        }
    });
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });
    google.maps.event.addListener(map, 'idle', loadPlaces);
}

google.maps.event.addDomListener(window, 'load', showGoogleMaps);
