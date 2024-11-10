(function () {
    'use strict';
    // this function is strict...
}());

function translate_static_words(farsi_string, translated_string) {
    // Get current site language
    var currentLanguage = document.querySelector('html').getAttribute('lang');
    if (currentLanguage === 'fa') {
        return farsi_string;
    } else {
        return translated_string;
    }
}

function copy(input) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(input).then(() => {
            return true;
        }, (err) => {
            return false;
        });
    } else if (window.clipboardData) {
        window.clipboardData.setData("Text", input);
        return true;
    } else {
        return false;
    }
}

function copy_text(e) {
    var tracking_code = e.getAttribute('data-val');
    copy(tracking_code);
    notification('success', translate_static_words('کد رهگیری کپی شد.', 'The tracking code was copied.'))
}