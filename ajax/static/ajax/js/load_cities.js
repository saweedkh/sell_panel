// load cities based on selected province
if ($('#id_address_form').length === 1) {
    $(document).on("change", "#id_province", function () {
        $.ajax({
            url: $('#id_address_form').data('load-cities-url'),
            type: "get",
            data: {'id_province': $('#id_province').val()},
            success: function (response) {
                $("#id_city").html(response)
            },
        });
    });
}

$(document).on("change", "#id_province_id", function () {

    $.ajax({
        url: $('#load-cities-url').data('load-cities-url'),
        type: "get",
        data: {'id_province': $('#id_province_id').val()},
        success: function (response) {
            $("#id_city_id").html(response)
        },
    });
});