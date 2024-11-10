window.addEventListener("load", function () {
    (function ($) {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $(document).ready(function () {
            if ($("#id_content_type").length) {
                const content_type_id = $('#id_content_type').val();

                // hide object id field if is empty
                if (content_type_id === '')
                    $('.form-row.field-object_id').hide();
                else
                    // change #id_object_id input href
                    ajax_set_link(content_type_id);

                // add lookup icon
                $('input#id_object_id').after('<a id="lookup_id_object_id" class="related-lookup" href="#">');

                $(document).on("change", "#id_content_type", function (e) {
                    e.preventDefault();
                    e.stopPropagation();

                    $('#id_object_id').val('')
                    const content_type_id = $('#id_content_type').val();

                    // show and hide object id field
                    if (content_type_id === '')
                        $('.form-row.field-object_id').hide();
                    else {
                        $('.form-row.field-object_id').show();
                        ajax_set_link(content_type_id);
                    }
                })

                function ajax_set_link(content_type_id) {
                    $.ajaxSetup({
                        beforeSend: function (xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        cache: true,
                    });

                    $.ajax({
                        url: '/menu/gfk-lookup-ajax/',
                        method: "POST",
                        data: {'content_type_id': content_type_id},
                        success: function (result) {
                            if (result.status === 200) {
                                // change 'href' of #id_object_id on content_type change
                                $('#lookup_id_object_id').attr('href', result.object_url);
                                console.log(result.object_url);
                                presentRelatedObjectModalOnClickOn('a.related-lookup', true);
                            }
                        },
                    });
                }
            }
        });

    })(django.jQuery);
});