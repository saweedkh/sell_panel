$(document).ready(function () {
    const inputArray = document.getElementsByClassName('upload-file');
    if (inputArray.length) {
        inputArray[0].addEventListener('change', prepareUpload, false);

        function prepareUpload() {
            if (this.files && this.files[0]) {
                let img = document.getElementById('image-data');
                img.src = URL.createObjectURL(this.files[0]);
            }
            document.getElementsByClassName('file-data')[0].classList.add('disabled');
        }
    }
})