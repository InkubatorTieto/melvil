    function show_reserved() {
        $("[id^='returnDetail']").css('display', 'none');
        $("[id^='reservDetail']").css('display', 'block');
        $(".borrowBtn").css('display', 'flex');
        $(".returnBtn").css('display', 'none');
        $("#returnDescrip").css('display', 'none');
        $("#reservDescrip").css('display', 'block');
        $("#paginReturn").css('display', 'none');
        $("#paginBorrow").css('display', 'flex');
        $("#showReserv").css('text-decoration', 'underline');
        $("#showReturn").css('text-decoration', 'none');
    }
    function show_borrowed() {
        $("[id^='reservDetail']").css('display', 'none');
        $("[id^='returnDetail']").css('display', 'block');
        $(".borrowBtn").css('display', 'none');
        $(".returnBtn").css('display', 'flex');
        $("#reservDescrip").css('display', 'none');
        $("#returnDescrip").css('display', 'block');
        $("#paginReturn").css('display', 'flex');
        $("#paginBorrow").css('display', 'none');
        $("#showReturn").css('text-decoration', 'underline');
        $("#showReserv").css('text-decoration', 'none');
    }

    $(document).ready(function(){
        var reservedBtn = $("#showReserv");
        var borrowedBtn = $("#showReturn");

        if (reservedBtn){
            reservedBtn.on("click", show_reserved);
        }
        if (borrowedBtn){
            borrowedBtn.on("click", show_borrowed);
        }
     });