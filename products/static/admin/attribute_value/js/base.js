window.addEventListener("load", function () {
    (function ($) {
        $(function () {
            if (window.location.href.includes('?_to_field=id') > -1) {
                $('#changelist-search .small.quiet').hide();
                $('#content-main .object-tools').hide();
            }
        });
    })(django.jQuery);
});