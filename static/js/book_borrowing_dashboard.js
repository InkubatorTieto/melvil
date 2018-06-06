    function reserved_books() {
        document.getElementById("booked_table").style.display = "none";
        document.getElementById("reserved_table").style.display = "block";
        document.getElementById("reserv_button").style.textDecoration = "underline";
        document.getElementById("booked_button").style.textDecoration = "none";
    }
    function booked_books() {
        document.getElementById("reserved_table").style.display = "none";
        document.getElementById("booked_table").style.display = "block";
        document.getElementById("reserv_button").style.textDecoration = "none";
        document.getElementById("booked_button").style.textDecoration = "underline";
    }

    window.onload = function() {
        var reservationButton = document.getElementById("reserv_button");
        var bookingButton = document.getElementById("booked_button");

        if (reservationButton){
            reservationButton.addEventListener("click", reserved_books);
        }
        if (bookingButton){
            bookingButton.addEventListener("click", booked_books);
        }
     }
