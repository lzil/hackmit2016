$(function()
{
    var fileInput = $("#upload");

    $(fileInput).on("change", function()
    {
        // actual file input stuff
        var fileInputVal = $(fileInput)[0].files[0];

        if (fileInputVal != ""){
            var reader = new FileReader();
            reader.readAsDataURL(fileInputVal);

            reader.onload = function()
            {
                var formData = new FormData();

                formData.append("file", reader.result);
                formData.append("filename", fileInputVal.name);

                var http = new XMLHttpRequest();
                http.open("POST", "/upload");
                http.send(formData);

                // reset input
                $(fileInput)[0].files = null;
            }
        }
    });

});

function previewFile()
{
    var preview = document.querySelector('#preview'); //selects the query named img
    var file = document.querySelector('input[type=file]').files[0]; //sames as here
    var reader = new FileReader();

    reader.onloadend = function()
    {
        preview.src = reader.result;
    }

    if (file)
    {
        reader.readAsDataURL(file); //reads the data as a URL
    }
    else
    {
        preview.src = "";
    }

    $("#preview").css(
    {
        opacity: 1
    });
}
