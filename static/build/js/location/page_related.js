/**
 * Created by xi on 2016-04-02.
 */

$('#search-place-input').focus(function () {
    $(this).animate({ width: "150%" }, 500);
});

$('#save_place').on('click', function() {
    $.ajax({
        url : "create_post/",
        type : "POST",
        data : { the_post : $('#post-text').val() }, // data sent with the post request
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});

$('#my_modal').on('show.bs.modal', function(e) {
    var bookId = $(e.relatedTarget).data('book-id');
    $(e.currentTarget).find('input[name="bookId"]').val(bookId);
});