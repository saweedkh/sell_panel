window.addEventListener("load", function () {
    (function ($) {
        $(function () {
            // Change order of items inline section
            $("#orderitem_set-group").insertBefore($('.module.aligned')[2]);

            // Hide variant field if order item already registered.
            $(".form-row.field-variant").each(function () {
                if ($(this).parent().parent().attr('id') !== 'orderitem_set-empty') {
                    if ($(this).find('input').val() !== '') {
                        $(this).hide();
                    }
                }
            });

            // Add variant link to product name.
            $(".inline-related.has_original.dynamic-orderitem_set").each(function () {
                var dynamicRawID = $(this).find("span[class=dynamic_raw_id_label][id*=orderitem_set-]");
                var selector = `span[class=dynamic_raw_id_label][id=${dynamicRawID.attr('id')}] > a`;
                waitForElm(selector).then((elm) => {
                    var variantLink = $(elm).attr('href');
                    var fieldName = $(this).find(".field-name");
                    var productName = fieldName.children().find('div').html();
                    fieldName.children().find('div').html(`<a target="_blank" href="${variantLink}">${productName}</a>`);
                });
            });

            var listOfElements = $(".field-prepayment");

            function toggleVerified(value) {
                if (value === '4') {
                    listOfElements.show();
                } else {
                    listOfElements.hide();
                }
            }

            // Get value of payment method field
            var paymentMethodField = $('#id_payment_method');

            // show/hide on load based on previous value of selectField
            toggleVerified(paymentMethodField.val());

            // show/hide on change
            paymentMethodField.change(function () {
                toggleVerified($(this).val());
            });

        });
    })(django.jQuery);
});

function copyToClipboard() {
    var copyText = document.getElementById("display_payment_link");
    navigator.clipboard.writeText(copyText.innerText);
}

function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}