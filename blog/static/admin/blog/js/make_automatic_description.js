function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
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
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

window.addEventListener("load", function () {
    (function ($) {
        // Get current site language
        var currentLanguage = $('html').attr('lang');

        $(document).ready(function () {
            var link;

            if (currentLanguage === 'fa-ir') {
                link = `<div class="help">برای <a type='button' id='id_automatic_description' style="cursor: pointer">ساخت خودکار توضیحات</a> کلیک کنید  </div><div class="help" id="error-automatic-description" style="color: red;"></div>`;
            } else {
                link = `<div class="help">Click to <a type='button' id='id_automatic_description' style="cursor: pointer">auto create description</a></div><div class="help" id="error-automatic-description" style="color: red;"></div>`;
            }
            $(".django-ckeditor-widget[data-field-id='id_description']").append(link)
        });

        $(document).on("click", '#id_automatic_description', function (e) {
            e.preventDefault();

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                cache: true,
            });

            var content_element = CKEDITOR.instances['id_content'];
            var description_element = CKEDITOR.instances['id_description'];
            var url = '/api/v1/blog/automate_description/';

            $.ajax({
                url: url,
                method: 'POST',
                data: {'content': content_element.getData()},
                success: function (data) {
                    if (data['status'] === 200) {
                        $("#error-automatic-description").html('')
                        description_element.setData(data['description'])
                    } else {
                        $("#error-automatic-description").html(data['message'])
                    }
                }
            });
        });
    })(django.jQuery);
});