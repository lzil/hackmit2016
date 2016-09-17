"""
    server.views
    ~~~~~~~~~~~~~~

    This module contains most of the views (read: non-error views)
    for our web app.

    :copyright: (c) 2016 whatever
    :license: lol don't steal this code pls
"""

import os
from flask import render_template, request, jsonify
from server import app, HOSTNAME

import base64
import cStringIO
from PIL import Image

# **********************************************************
# FILE UPLOADING
# **********************************************************

UPLOAD_FOLDER = "uploads"

# separates file extension and checks if is an image file
ALLOWED_EXTENSIONS = set(['png','tiff','tif','jpg','jpeg','JPG','TIFF','TIF','PNG'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# b64: base64 encoded string
# return: decoded version of b64 with tag removed
def decodeB64(b64):
    str = b64.replace('data:image/png;base64,', '') #replace tag
    decoded = base64.b64decode(str)
    return decoded

# imgData: raw image data in string form
# return: PIL object containing the image, or None
def encodePIL(imgData):
    try:
        str = cStringIO.StringIO()              # PIL only accepts weird formats
        str.write(imgData)                      # so make it a cStringIO
        img = Image.open(str)                   # open Image by str data
        return img                              # a pickled image? how sour
    except:
        return None;

# file uploading backend
@app.route("/upload", methods=['POST'])
def upload():
    fileObj = request.form['file']
    filename = request.form['filename']

    if fileObj and allowed_file(filename):
        fileDec = decodeB64(fileObj)
        fileImg = encodePIL(fileDec)

        fullpath = os.path.join(UPLOAD_FOLDER, filename)
        fileImg.save(fullpath)

    num = 0
    return jsonify(score=num)

@app.route("/", methods=['GET', 'POST'])
def index():
    """ Our homepage! """
    return render_template('home.html')
