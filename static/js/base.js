console.log("Javascript here:");
// <script>
$(document).ready(function () {
    $("#txtSearch").autocomplete({
        source: "/ajax_calls/search/",
        minLength: 2,
        open: function () {
            setTimeout(function () {
                $('.ui-autocomplete').css('z-index', 99);
            }, 0);
        }
    });
});
