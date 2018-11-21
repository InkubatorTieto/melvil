    function show_reserved() {
        $(".borrowBtn").css('display', 'flex');
        $(".returnBtn").css('display', 'none');
        $("#myReserv").show();
        $("#myBorrows").hide();
        $("#paginReturn").css('display', 'none');
        $("#paginBorrow").css('display', 'flex');
    }
    function show_borrowed() {
        $(".borrowBtn").css('display', 'none');
        $(".returnBtn").css('display', 'flex');
        $("#myReserv").hide();
        $("#myBorrows").show();
        $("#paginReturn").css('display', 'flex');
        $("#paginBorrow").css('display', 'none');
    }

    $(document).ready(function(){
        var reservedBtn = $("#showReserv");
        var borrowedBtn = $("#showReturn");
        var mystart = 0;

        if (reservedBtn){
            reservedBtn.on("click", show_reserved);
        }
        if (borrowedBtn){
            borrowedBtn.on("click", show_borrowed);
        }

        if (mystart === 0){
            show_reserved();
            mystart = 1;
        }
     });