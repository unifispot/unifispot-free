import os
from werkzeug.utils import secure_filename
from flask import url_for
import time
from PIL import Image

def handleUpload(app, file,thumbsize=32):
    """ Generic handler for uploading file, Need to pass app context and file
        Based on https://bitbucket.org/adampetrovic/flask-uploader/
        And http://stackoverflow.com/questions/17584328/any-current-examples-using-flask-and-jquery-file-upload-by-blueimp

    """
    if not file:
        return None
    if file:
        filename = time.strftime('%Y%m%d-%H%M%S') + '-' + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        generate_and_save_thumbnail(app, filename,thumbsize)
        print filename
        fileurl = url_for('upload.download_file', filename=filename)
        thumburl = url_for('upload.download_file', filename='thumbs/' + filename)
    return {'url': fileurl,
     'thumb': thumburl}


def generate_and_save_thumbnail(app, filename,thumbsize):
    myimage = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    myimage = myimage.resize((thumbsize,thumbsize ), Image.ANTIALIAS)
    myimage.save(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbs', filename))

