window.addEventListener("load", function () {
    (function ($) {
        $(document).ready(function () {
            var word = translate_static_words('ساخت کد تصادفی', 'Generate random code');
            $('#id_code.vTextField').after(`<button type="button" id="id_generate_code" class="button">${word}</button>`);

            $('#id_generate_code').on('click', function (e) {
                var length = 7;
                $('#id_code.vTextField').val(create_code(length));
            });
        });

        function create_code(length) {
            var result = '';
            var characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
            var charactersLength = characters.length
            for (var i = 0; i < length; i++) {
                result += characters.charAt(Math.floor(Math.random() * charactersLength));
            }
            return result;
        }

        function translate_static_words(farsi_string, translated_string) {
            // Get current site language
            var currentLanguage = $('html').attr('lang');
            if (currentLanguage === 'fa') {
                return farsi_string;
            } else {
                return translated_string;
            }
        }

    })(django.jQuery);
});

