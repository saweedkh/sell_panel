$(document).on("keyup", '.persian_digit', function (e) {
    var ctrlKey = 67, vKey = 86;
    if (e.keyCode != ctrlKey && e.keyCode != vKey) {
        $(this).val(persianToEnglish($(this).val()));
    }
});

function persianToEnglish(input) {
    var inputstring = input;
    var persian = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
    var english = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
    for (var i = 0; i < 10; i++) {
        var regex = new RegExp(persian[i], 'g');
        inputstring = inputstring.toString().replace(regex, english[i]);
    }
    return inputstring;
}