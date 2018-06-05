$(function() {
    $.ajax({
        url: '/wishlist',
        type: 'GET',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
})