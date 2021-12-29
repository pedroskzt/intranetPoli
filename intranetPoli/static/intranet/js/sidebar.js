$(document).ready(function () {
            $('#dismiss, #overlay').on('click', function () {
                $('#sidebar').removeClass('active');
                document.getElementById("overlay").style.display = "none";
            });

            $('#sidebarCollapse').on('click', function () {
                $('#sidebar').addClass('active');
                $('.collapse.in').toggleClass('in');
                document.getElementById("overlay").style.display = "block";

                $('a[aria-expanded=true]').attr('aria-expanded', 'false');
            });
        });