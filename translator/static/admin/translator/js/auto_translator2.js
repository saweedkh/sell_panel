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
        var myButtons;
        var translateTarget = [];
        var InReg = /(?<=.{2})\w\w$/;
        var ajax_data;
        var text_element;
        var contentLabel;
        var clean_data = $('<div>');
        var url = '/en/translator/';
        var loadingSpan;
        var warningElement;


        function setMyLanguage(lan, myCk, errorClass) {
            translateTarget.push(lan);
            $(".dialog-content").hide();
            sendRequestToServer(myCk, errorClass)
            translateTarget = [];

        }

        $(document).ready(function () {
            var link;

            if (currentLanguage === 'fa') {
                link = `<div>
                        <div class="help" style="margin-right: 0px">برای 
                        <a type='button' class='id_automatic_translate' id='id_automatic_translate' style="cursor: pointer">ساخت خودکار ترجمه</a> کلیک کنید  
                           <div class="help translator-warning" title="این متن به صورت ماشینی ترجمه شده است.امکان اشکال در ترجمه وجود دارد!" id="translator-warning" style="font-size: 12px; display: none;color: var(--admin-interface-generic-link-color);margin-right: 0px">
                        ⚠️
                        </div>
                        </div>
                        <span class="help translatorLoading" style="display: none;color: var(--admin-interface-generic-link-color); margin-right: 10px">
                        <img src="/static/translator/images/load.gif" style="width: 16px; height: 16px; margin-right: 10px">در حال ترجمه...
                        </span>
                        <div class="help" id="error-automatic-translator" style="color: red; margin-right: 0px"></div>
                        <div class="dialog-content" id="dialog-content" style="margin-right: 10px"></div>
                        </div>`;
            } else {
                link = `<div>
                        <div class="help" style="margin-left: 0px">Click to 
                        <a type='button' class='id_automatic_translate' style="cursor: pointer">
                        auto create translation
                        </a>
                             <div class="help translator-warning" title="This text has been translated by machine. There may be errors in the translation!" id="translator-warning" style="font-size: 12px; display: none;color: var(--admin-interface-generic-link-color);margin-left: 0px">
                        ⚠️
                        </div>
                        </div>
                        <span class="help" class="translatorLoading" style="color: #0C3C26" ></span>
                        <span class="help translatorLoading" style="display: none;color: var(--admin-interface-generic-link-color); margin-right: 10px">
                        <img src="/static/translator/images/load.gif" style="width: 16px; height: 16px; margin-right: 10px">
                        translating...</span>
                        <div class="help" id="error-automatic-translator" style="color: red; margin-left: 0px"></div>
                        <div class="dialog-content" id="dialog-content" style="margin-left: 10px"></div>
                        
                        </div>`;
            }
            var uiTabs = $(".ui-tabs");

            uiTabs.each(function () {
                $(this).attr('data-btn_created', false);
                if ($(this).find('input[type="file"]').length === 0) {
                    $(this).append(link);
                }
            })

        });


        $(document).on("click", '.id_automatic_translate', function () {
            // e.preventDefault();

            var btnContent = $(this).parent().parent().find('.dialog-content');
            btnContent.show();
            var warningElement = $(this).parent().parent().find('.translator-warning');
            warningElement.css('display', 'inline');

            var InReg = /(?<=.{2})\w\w$/;
            text_element = $(this).parent().parent().parent().find('input, textarea');
            contentLabel = $(this).parent().parent().parent().find('label');
            var uiTab = $(this).parent().parent().parent();

            text_element.each(function () {
                var btnId = $(this).attr('id').match(InReg);
                if (uiTab.attr('data-btn_created') === 'false') {

                    if ($('html').attr('lang') != btnId) {
                        var myBtn = `<button class="lan-btn translation-buttons" type="button" id="${btnId}" style="background-color:#f8f9fa; border: 1px solid #b9b9b9; border-radius:4px; color: #3c4043; margin: 2px; width: 50px">${btnId}</button>`;
                        var $button = $(myBtn); // Convert the HTML string to a jQuery object

                        // $(".dialog-content").append($button);
                        btnContent.append($button);
                    } else {
                        var allLanBtn = `<button class="translation-buttons" id="all-lan" type="button" style="background-color:#f8f9fa; border: 1px solid #b9b9b9; border-radius:4px; color: #3c4043; margin: 2px; width: 50px" >all</button>`;
                        btnContent.append(allLanBtn);

                    }
                }

            })
            uiTab.attr('data-btn_created', true);
            myButtons = btnContent.find('button');
        });

        $(document).on('click', '.translation-buttons', function (e) {
            loadingSpan = $(this).parent().parent().find('span');
            loadingSpan.show()
            var errorClass = $(this).parent().parent().find('#error-automatic-translator');

            var selectedLan = [];
            var translationButtons = $('.lan-btn')

            try {
                var myCk = CKEDITOR.instances[contentLabel.attr('for')];
            } catch (error) {
                var myCk = undefined;
            }


            e.preventDefault();
            var target = e.target;
            var $jTarget = $(target);
            if ($jTarget.attr('id') === $(this).attr('id') && $jTarget.attr('id') !== 'all-lan') {
                selectedLan.push($jTarget.attr('id'))
                setMyLanguage(selectedLan, myCk, errorClass);
                selectedLan = [];


            } else if ($jTarget.attr('id') === 'all-lan' && $(this).attr('id') === 'all-lan') {
                // translateTarget.push(text_element.match(InReg))
                for (var i = 0; i < translationButtons.length; i++) {
                    var btnCode = translationButtons[i];
                    var $btnCode = $(btnCode).attr('id');
                    selectedLan.push($btnCode);
                }
                setMyLanguage(selectedLan, myCk, errorClass);
                selectedLan = [];

            }
        })

        function sendRequestToServer(myCk, errorClass) {
            if (myCk !== undefined) {
                ajax_data = myCk.getData();

            } else {
                ajax_data = text_element.val();
            }

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }, cache: true,
            });
            $.ajax({
                url: url,
                method: 'POST',
                data: {
                    'text': ajax_data,
                    'targets': translateTarget.toString()
                },

                success: function (data) {
                    if (data['status'] === 200) {
                        errorClass.html('')
                        var context = data['context']
                        if (myCk !== undefined) {
                            var currentCk;
                            contentLabel.each(function () {
                                var inputsId = $(this).attr('for');
                                currentCk = CKEDITOR.instances[inputsId];
                                var getLanInp = inputsId.match(InReg);
                                for (var language in context) {
                                    if (getLanInp == language) {
                                        if (clean_data.html(currentCk.getData()).text() == clean_data.html(myCk.getData()).text() || clean_data.html(currentCk.getData()).text() != '') {
                                            var confResult = confirm(`فیلد شما خالی نسیت. آیا مایل هستید که مقدار ترجمه شده را جایگزین مقدار فعلی ${getLanInp} کنید؟`);
                                            if (confResult) {
                                                // $(this).html(context[language]);
                                                currentCk.setData(context[language]);
                                            }
                                        } else {
                                            currentCk.setData(context[language]);
                                        }
                                    }
                                }
                                currentCk = null;
                            });

                        } else {
                            text_element.each(function () {
                                var inputsId = $(this).attr('id');
                                var getLanInp = inputsId.match(InReg);
                                for (var language in context) {
                                    if (getLanInp == language) {
                                        if (clean_data.html($(this).val()).text() == clean_data.html(text_element.val()).text() || clean_data.html($(this).val()).text() != '') {
                                            var confResult = confirm(`فیلد شما خالی نسیت. آیا مایل هستید که مقدار ترجمه شده را جایگزین مقدار فعلی${getLanInp} کنید؟`);
                                            if (confResult === true) {
                                                $(this).val(context[language] + translateTarget);
                                            }

                                        } else {
                                            $(this).val(context[language])
                                        }
                                    }
                                }
                            });
                        }

                        loadingSpan.hide();
                        $('.translator-warning').css('display', 'none');


                    } else {
                        loadingSpan.hide();
                        $('.translator-warning').css('display', 'none');
                        errorClass.html(data['message']);
                    }
                },

            });
            translateTarget = [];
        }

    })(django.jQuery);

});
