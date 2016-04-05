var map;
var markers = [];
var selected_markers = [];
var iconBase = '../static/build/images/';
var icons = {
  default: {
    icon: iconBase + 'map_marker.png'
  },
  unselect: {
    icon: iconBase + 'library_maps.png'
  },
  info: {
    icon: iconBase + 'info-i_maps.png'
  }
};

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
                    icon: iconBase + 'map_marker.png'
                });

                markers.push(marker);

                google.maps.event.addListener(markers[i], "click", function (e) {
                    var infoBox = new InfoBox({
                        latlng: this.getPosition(),
                        map: map,
                        //content: this.content
                    });
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

    loadPlaces(map);
    google.maps.event.addListener(map, 'idle', function(ev){

    });
}

google.maps.event.addDomListener(window, 'load', showGoogleMaps);
