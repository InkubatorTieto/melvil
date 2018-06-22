    function reserved_books() {
        $("#booked_table").css('display', 'none');
        $("#reserved_table").css('display', 'block');
        $("#reserv_button").css('text-decoration', 'underline');
        $("#booked_button").css('text-decoration', 'none');
    }
    function booked_books() {
        $("#reserved_table").css('display', 'none');
        $("#booked_table").css('display', 'block');
        $("#booked_button").css('text-decoration', 'underline');
        $("#reserv_button").css('text-decoration', 'none');
    }

    $( document ).ready(function(){
        var reservationButton = $("#reserv_button");
        var bookingButton = $("#booked_button");

        if (reservationButton){
            reservationButton.on("click", reserved_books);
        }
        if (bookingButton){
            bookingButton.on("click", booked_books);
        }
     });
