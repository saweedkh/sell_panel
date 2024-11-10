function print_invoice() {
    $("#printable").printThis();
}

$(function () {
    print_invoice();
    $("#print_invoice").click(print_invoice);
});