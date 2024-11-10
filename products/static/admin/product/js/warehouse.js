window.addEventListener("load", function () {
    (function ($) {
        $(function () {
            // Get current site language
            var currentLanguage = $('html').attr('lang');

            // Persianize Warehouse admin page

            if (currentLanguage === 'fa') {
                $("div .admin-numeric-filter-wrapper button").each(function (index, element) {
                    $(this).html('اعمال');
                });

                $("div .admin-numeric-filter-wrapper h3").each(function (index, element) {
                    if (index === 0) {
                        $(this).html('توسط موجودی');
                    }
                });

                $("div .admin-numeric-filter-wrapper input").each(function (index, element) {
                    if ($(this).attr('placeholder') === 'From') {
                        $(this).attr('placeholder', 'از')
                    }
                    if ($(this).attr('placeholder') === 'To') {
                        $(this).attr('placeholder', 'تا')
                    }
                });
            }

        });
    })(django.jQuery);
});