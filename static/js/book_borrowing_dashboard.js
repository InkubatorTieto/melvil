    function reserved_books() {
        $("#booked_table").hide();
        $("#reserved_table").show();
        $("#reserv_button").css('text-decoration', 'underline');
        $("#booked_button").css('text-decoration', 'none');
    }
    function booked_books() {
        $("#reserved_table").hide();
        $("#booked_table").show();
        $("#booked_button").css('text-decoration', 'underline');
        $("#reserv_button").css('text-decoration', 'none');
    }

    $( document ).ready(function(){
        var reservationButton = $("#reserv_button");
        var bookingButton = $("#booked_button");
        var mystart = false;
        if (reservationButton){
            reservationButton.on("click", reserved_books);
        }
        if (bookingButton){
            bookingButton.on("click", booked_books);
        }

         if (mystart === false){
            reserved_books();
            mystart = true;
        }
     });
