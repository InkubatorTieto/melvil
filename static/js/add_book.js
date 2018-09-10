
    function showMagazine() {
        $("#magazine_form").show();
    }

    function hideBooks() {
        $("#book_form").hide();
    }

    function hideMagazine() {
        $("#magazine_form").hide();
    }

    function showBooks() {
        $("#book_form").show();
    }

    function set_checked_form() {
        var radioValue = $("input[name='item_category']:checked").val();
            if (radioValue == 'magazine') {
                hideBooks();
                showMagazine();
            }
            if (radioValue == 'book') {
                hideMagazine();
                showBooks();
            }
        }

    $(document).ready(function () {
        set_checked_form();
        $("input[name='item_category']").click(function () {
            set_checked_form();
        });
    });
