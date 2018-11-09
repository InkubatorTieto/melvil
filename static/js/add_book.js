
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
        var radioValue = $("input[name='radio']:checked").val();
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
        $("input[name='radio']").click(function () {
            set_checked_form();
        });
    });
