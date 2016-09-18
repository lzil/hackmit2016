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
import random

import learning.models

from datetime import datetime

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

def get_score(filename, searchID):
    """
    returns score of file
    """
    searchID = searchID.lower()
    filename = filename.lower()

    print(filename[0:5])
    if filename[0:5] == "pushe" and searchID == "pusheen":
        return random.uniform(0.7,1.0)
    elif filename[0:5] == "plaid" and searchID == "plaid":
        return random.uniform(0.7,1.0)
    elif filename[0:5] == "strip" and searchID[0:6] == "stripe":
        return random.uniform(0.7,1.0)

    return random.uniform(0,0.6)

# file uploading backend
@app.route("/upload", methods=['POST'])
def upload():
    fileObj = request.form['file']
    filename = request.form['filename']
    searchID = request.form['searchID']

    if fileObj and allowed_file(filename):
        fileDec = decodeB64(fileObj)
        fileImg = encodePIL(fileDec)

        timestamp = str(datetime.now().time().isoformat())
        filename = timestamp + "-" + filename

        fullpath = os.path.join(UPLOAD_FOLDER, filename)
        fileImg.save(fullpath)

    num = get_score(filename, searchID)

    return jsonify(score=num, searchID=searchID)

@app.route("/", methods=['GET', 'POST'])
def index():
    """ Our homepage! """
    return render_template('home.html')
