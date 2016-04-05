/**
 * Created by xi on 2016-04-02.
 */

var geocoder = new google.maps.Geocoder();

$("#search-place-input").keyup(function(event){
    if(event.keyCode == 13){
        searchPlace();
    }
});

function searchPlace() {
    var address = document.getElementById("search-place-input").value;
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var location = results[0].geometry.location;
            map.setCenter(location);
            var marker = new google.maps.Marker({
                map: map,
                position: location,
                icon: iconPath + 'map_marker_blue.png'
            });
            if (results[0].geometry.viewport) {
                map.fitBounds(results[0].geometry.viewport);
            }

            var contentString = "<div><button type='button' class='btn btn-primary btn-lg' data-toggle='modal' data-target='#myModal'>Add</button></div>";
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });
            infowindow.open(map, marker);

            $('#inputName').val(results[0].address_components[0].long_name);
            $('#inputLat3').val(location.lat);
            $('#inputLng3').val(location.lng);
            $('#inputAddr').val(results[0].searchPlace);
            $('#inputPlaceId').val(results[0].place_id);

        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}

