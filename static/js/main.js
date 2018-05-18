function nav_buttons_activate(){
          switch(window.location.pathname) {
            case "/":
                var login = document.getElementById("home");
                home.classList.add("active");
                break;
            case "/register":
                var register = document.getElementById("register");
                register.classList.add("active");
                break;
            case "/login":
                var login = document.getElementById("login");
                login.classList.add("active");
                break;
            case "/search":
                var search = document.getElementById("search");
                search.classList.add("active");
                break;
            case "/contact":
                var contact = document.getElementById("contact");
                contact.classList.add("active");
                break;
            }
        }

window.onload = nav_buttons_activate;