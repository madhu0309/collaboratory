jQuery(function () {
    $("#id_input").on('keyup', function () {
        var value = $(this).val();
        $.ajax({
            url: "{% collab_app:question_list %}",
            data: {
                'search': value
            },
            dataType: 'json',
            success: function (data) {
                list = data.list;
                $("#id_input").autocomplete({
                    source: list,
                    minLength: 3
                });
            }
        });
    });
});