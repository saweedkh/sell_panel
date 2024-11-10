window.addEventListener("load", function () {
    (function ($) {
        $(function () {
            var currentLanguage = $('html').attr('lang');

            let main_formset = $("#id_productspecification_set-TOTAL_FORMS").closest("fieldset");

            let button_text;
            if (currentLanguage === 'fa') {

                button_text = 'بارگذاری ویژگی ها';
            } else {
                button_text = 'Load attributes';
            }

            main_formset.find('h2').prepend(`<input type="button" id="get_attributes" value="${button_text}">`);

            let categories = $('#id_category').val()

            $(document).on("click", "#get_attributes", function () {
                $.ajax({
                    url: '/create_specification_form/',
                    method: 'GET',
                    data: {'categories_id': categories},
                    success: function (data) {
                        main_formset.append(data);
                        $('#id_productspecification_set-TOTAL_FORMS').val($('.dynamic-productspecification_set').length)
                    }
                });
            });

        });
    })(django.jQuery);
});