window.addEventListener("load", function () {
    (function ($) {
        $(function () {

            // Default checkboxes
            var default_checkboxes = '#variant_set-group input:checkbox[name$="-default"]';

            // Select just one default checkbox
            $(document).on('click', default_checkboxes, function () {
                $(default_checkboxes).not(this).prop('checked', false);
            });

            // Change order of variant inline section
            $("#variant_set-group").insertBefore($('.module.aligned')[1]);
            // Get value of product type field
            var typeField = $('#id_type');
            // Hide/Show element by product type status
            var listOfElements = $(
                ".form-row.field-attributes," +
                "#variant_set-group .inline-related.has_original.dynamic-variant_set h3," +
                "#variant_set-group .form-row.field-attribute_values," +
                "#variant_set-group .form-row.field-image," +
                "#variant_set-group .form-row.field-default," +
                "#variant_set-group th:last-child," +
                "#variant_set-group .delete," +
                "#variant_set-group .add-row," +
                "#variant_set-group .original"
            );



            if ($("#variant_set-group input:checkbox:not(:checked)[name$='-default']").length <= 0){
                var defaultVariantLine = $("#variant_set-group input:checkbox:not(:checked)[name$='-default']").closest(".inline-related.has_original.dynamic-variant_set");
            }else{
                var defaultVariantLine = $("#variant_set-group").closest(".inline-related.has_original.dynamic-variant_set");
            }

            var variantLines = $(default_checkboxes);

            // Change title of variant inline section by product type status
            var variantSectionTitle = $('#variant_set-group .module h2').first();
            // Get current site language
            var currentLanguage = $('html').attr('lang');


            function toggleVerified(value) {
                if (value === '1') {
                    defaultVariantLine.show();
                    listOfElements.show();
                    if (currentLanguage === 'fa') {
                        variantSectionTitle.text('تنوع محصولات');
                    } else {
                        variantSectionTitle.text('Product Variant');
                    }
                } else {
                    $('.inline-related.last-related.dynamic-variant_set').remove()
                    $('#id_variant_set-TOTAL_FORMS').val('1')
                    defaultVariantLine.hide();
                    listOfElements.hide();
                    if (window.location.href.indexOf('product/add/') > -1) {
                        variantLines.prop('checked', true);
                    }
                    if (currentLanguage === 'fa') {
                        variantSectionTitle.text('اطلاعات محصول');
                    } else {
                        variantSectionTitle.text('Product Information');
                    }
                }
            }

            // show/hide on load based on pervious value of selectField
            toggleVerified(typeField.val());

            // show/hide on change
            typeField.change(function () {
                toggleVerified($(this).val());
            });


            // Change Attribute Value
            var attribute_field = $('#id_attribute');
            toggleAttribute(attribute_field.val());
            attribute_field.change(function () {
                toggleAttribute($(this).val());

                if ($(this).value !== '0') {

                    $("input[id$=-attribute_value][class=vForeignKeyRawIdAdminField]").each(function () {
                        $(this).val('');

                    });

                    $("span[id$=-attribute_value_dynamic_raw_id_label][class=dynamic_raw_id_label]").each(function () {
                        $(this).html('&nbsp;');
                    });
                }

            });

            function toggleAttribute(value) {
                $("a[id$=-attribute_value][class=dynamic_raw_id-related-lookup]").each(function () {
                    if (value !== '') {
                        this.href = this.href + '&attribute__id__exact=' + value;
                    }
                });
            }

            // Add Recommend products button
            var get_related_products_text = ((currentLanguage === 'fa') ? 'پیشنهاد محصولات' : 'Recommend products');
            $("#related_from-group fieldset h2").append(`<p id="fill_related_prodcuts" class="btn-in-header">${get_related_products_text}</p>`);


            // Extract the ID from the URL using regular expressions
            var pageUrl = window.location.href;
            var regex = /\/(\d+)\/change\/$/;
            var match = pageUrl.match(regex);
            var objectId = match ? match[1] : null;

            $(document).on("click", "#fill_related_prodcuts", function () {

                if (objectId) {
                    const url = `/fill-related-products/${objectId}`;

                    $.ajax({
                        url: url,
                        type: "get",
                        success: function (response) {
                            var totalForms = $('#id_related_from-TOTAL_FORMS').val();

                            response.data.forEach(function (item, index) {
                                var forloopCounter = parseInt(index) + parseInt(totalForms);
                                var newInline = $('#related_from-empty').clone();
                                newInline.attr("id", `related_from-${forloopCounter}`);
                                newInline.removeClass('empty-form').addClass('dynamic-related_from');
                                newInline.html(newInline.html().replaceAll("__prefix__", forloopCounter));
                                newInline.find(`#id_related_from-${forloopCounter}-to_product`).val(item.id)
                                newInline.find('.related-widget-wrapper').append(`<span class="dynamic_raw_id_label" id="related_from-${forloopCounter}-to_product_dynamic_raw_id_label"> <a href="${item.url}">${item.name}</a></span>`)
                                $("#related_from-empty").before(newInline);
                            });

                            var sum = parseInt(totalForms) + parseInt(response.data.length);
                            totalForms.val(sum);
                        },
                    });
                }
            });

        });
    })(django.jQuery);
});