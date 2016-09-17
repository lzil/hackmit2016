$(function() {

    var results = document.getElementsByClassName ('box');
    results.innerHTML = 'Drag and drop an image to start.';
    
    var box = document.getElementsByClassName ('box'),
        tests = {
            filereader: typeof FileReader != 'undefined',
            dnd: 'draggable' in document.createElement('span'),
            formdata: !!window.FormData,
            progress: "upload" in new XMLHttpRequest
        },
        support = {
            filereader: document.getElementById('filereader'),
            formdata: document.getElementById('formdata'),
            progress: document.getElementById('progress')
        },
        acceptedTypes = {
            'image/png': true,
            'image/jpeg': true,
            'image/gif': true
        },
        progress = document.getElementById('uploadprogress'),
        fileupload = document.getElementById('upload');

    "filereader formdata progress".split(' ').forEach(function(api) {
        if (tests[api] === false) {
            support[api].className = 'fail';
        } else {
            // FFS. I could have done el.hidden = true, but IE doesn't support
            // hidden, so I tried to create a polyfill that would extend the
            // Element.prototype, but then IE10 doesn't even give me access
            // to the Element object. Brilliant.
            support[api].className = 'hidden';
        }
    });

    function previewfile(file) {
        if (tests.filereader === true && acceptedTypes[file.type] === true) {
            var reader = new FileReader();
            reader.onload = function(event) {
                var image = new Image();
                image.src = event.target.result;
                image.width = 500; // a fake resize
                box.innerHTML = '';
                box.appendChild(image);
            };

            reader.readAsDataURL(file);
        } else {
            box.innerHTML += '<p>Uploaded ' + file.name + ' ' + (file.size ? (file.size / 1024 | 0) + 'K' : '');
            console.log(file);
        }
    }

    function readfiles(files) {
        //debugger;
        var formData = tests.formdata ? new FormData() : null;
        for (var i = 0; i < files.length; i++) {
            if (tests.formdata) {
                formData.append('ID', 'demo');
                formData.append('file', files[i]);
            }
            previewfile(files[i]);
            result.innerHTML = 'Uploading and Processing Image...';
        }

        // now post a new XHR request
        if (tests.formdata) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/v1/uploadImage');
            xhr.onload = function() {
                progress.value = progress.innerHTML = 100;
            };
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    var results = JSON.parse(xhr.responseText);
                    if (results.database_id === 0) { // not logged in
                        result.innerHTML = 'Please authenticate to access API.' + '</p>';
                    } else {
                        result.innerHTML = '<p>Estimated severity: ' + results.grade.slice(1, 6) + '</p>';
                    }
                    progress.value = progress.innerHTML = 0;
                }
            }

            if (tests.progress) {
                xhr.upload.onprogress = function(event) {
                    if (event.lengthComputable) {
                        var complete = (event.loaded / event.total * 100 | 0);
                        progress.value = progress.innerHTML = complete;
                    }
                }
            }

            xhr.send(formData);
        }

        // on complete send a get request for result
    }

    if (tests.dnd) {
        box.ondragover = function() {
            this.className = 'hover';
            return false;
        };
        box.ondragend = function() {
            this.className = '';
            return false;
        };
        box.ondrop = function(e) {
            this.className = '';
            e.preventDefault();
            readfiles(e.dataTransfer.files);
        }
    } else {
        fileupload.className = 'hidden';
        fileupload.querySelector('input').onchange = function() {
            readfiles(this.files);
        };
    }

});