/**
 * Created by xi on 2016-04-02.
 */

//$('#search-place-input').focus(function () {
//    $(this).animate({ width: "150%" }, 500);
//});

$('#save_place').on('click', function() {
    $.ajax({
        url : "create_place/",
        type : "POST",
        data : $('#add-location-form').serialize(),
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            focused_markers.setMap(null);
            var latlng = json.latlng;
            var place_id = json.place_id;
            var marker = new google.maps.Marker({
                map: map,
                place_id: place_id,
                position: {lat: latlng[0], lng: latlng[1]},
                icon: iconBase + 'Marker_balck.png'
            });
            markers.push(unselected_marker);
        },
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});

function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i -= 1) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

function process_route(best_route_pre_process) {
    return best_route_pre_process.map(function(item, index) {
        return {lat: item[0], lng: item[1]};
    });
}

$('#save_route').on('click', function() {
    var points = selected_markers.map(function(item, index) {
        return [item.position.lat(), item.position.lng()];
    });
    shuffle(points);
    var best_route_pre_process = init_graph(points);
    var best_route_post_process = process_route(best_route_pre_process);
    if (route) {
        route.setMap(null);
    }
    route = new google.maps.Polyline({
        path: best_route_post_process,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    route.setMap(map);
});


$('#my_modal').on('show.bs.modal', function(e) {
    var bookId = $(e.relatedTarget).data('book-id');
    $(e.currentTarget).find('input[name="bookId"]').val(bookId);
});


//success : function(json) {
//    $('#post-text').val(''); // remove the value from the input
//    $("#talk").prepend("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+"</span></li>");
//},