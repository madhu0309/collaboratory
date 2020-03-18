jQuery(function () {
    $("#id_input").on('keyup', function () {
        var value = $(this).val();
        console.log(value)
        $.ajax({
            url: "",
            data: {
                'search': value
            },
            dataType: 'json',
            success: function (data) {
                list = data.list;
                console.log("Success");
                $("#id_input").autocomplete({
                    source: list,
                    minLength: 3
                });
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
        });
    });
});
