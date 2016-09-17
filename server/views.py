"""
    server.views
    ~~~~~~~~~~~~~~

    This module contains most of the views (read: non-error views)
    for our web app.

    :copyright: (c) 2016 whatever
    :license: lol don't steal this code pls
"""

from flask import render_template, request
from server import app, HOSTNAME

# **********************************************************
# FILE UPLOADING
# **********************************************************

# separates file extension and checks if is an image file
ALLOWED_EXTENSIONS = set(['png','tiff','tif','jpg','jpeg','JPG','TIFF','TIF','PNG'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# file uploading backend
@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        pass

    num = 0

    return jsonify(score=num)

@app.route("/", methods=['GET', 'POST'])
def index():
    """ Our homepage! """
    return render_template('home.html')
