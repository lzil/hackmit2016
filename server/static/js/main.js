$(function()
{
    // aesthetics
    $(".header a img").on("mouseover", function(){
        $(this).attr("src", "/static/img/logo.png");
    });
    $(".header a img").on("mouseout", function(){
        $(this).attr("src", "/static/img/logo2.png");
    });
    
    var fileInput = $("#upload");

    $(fileInput).on("change", function()
    {
        sendRequest();
    });

    $("#queryID").on("focusout", function()
    {
        sendRequest();
    });
});

function sendRequest()
{
    var fileInput = $("#upload");
    // actual file input stuff
    var fileInputVal = $(fileInput)[0].files[0];
    // query string
    var searchID = $("#queryID").val();
    
    if (fileInputVal != "" && searchID != "")
    {
        var reader = new FileReader();

        reader.onloadend = function()
        {
            var formData = new FormData();

            formData.append("file", reader.result);
            formData.append("filename", fileInputVal.name);
            formData.append("searchID", searchID);

            $.ajax({
                data: formData,
                url: "/upload",
                method: 'POST',
                contentType: false,
                processData: false,
                success: function(data, status, jqxhr) {
                    displayResults(data);
                }
            });
            
            // reset input
            $(fileInput)[0].files = null;
        }
        
        reader.readAsDataURL(fileInputVal);
    }
}

// displays results nicely
function displayResults(data)
{
    $("#upload-visible").hide();
    $("#descriptions").hide();
    
    // $("#box").css("display","inline-block");
    // $("#score").css("display","inline-block");
    
    $("#box").fadeIn();
    $("#score").fadeIn();
    
    var score = data.score;
    $("#score").html("Very much Pusheen!! Score: " + score);
}

function previewImg(img)
{
    var canvas = document.getElementsByTagName("canvas")[0];
    var holder = $("#box");
    
    // resize img so that longest size is at max, 256
    var MAX_WIDTH = 256;
    var MAX_HEIGHT = 256;
    var width = img.width;
    var height = img.height;

    if (width > height)
    {
        if (width > MAX_WIDTH)
        {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
        }
    }
    else
    {
        if (height > MAX_HEIGHT)
        {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
        }
    }

    canvas.width = width;
    canvas.height = height;

    var ctx = canvas.getContext("2d");
    // ctx.drawImage(img, 0, 0, width, height);

    var dataurl = canvas.toDataURL();
    
    return dataurl;
}

function previewFile()
{
    var preview = document.querySelector('#preview'); //selects the query named img
    var file = document.querySelector('input[type=file]').files[0]; //sames as here
    var reader = new FileReader();

    reader.onloadend = function()
    {
        preview.src = reader.result;
        previewImg(preview);
    }

    if (file)
    {
        reader.readAsDataURL(file); //reads the data as a URL
    }
    else
    {
        // preview.src = "";
    }

    $("#preview").css(
    {
        opacity: 1
    });
}