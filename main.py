import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from random import randint
import numpy
import sys
from helper import *
from encrypt import encrypt_image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def upload_form():
    return render_template('upload.html')




# gets the image in and encrypts it properly

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file found')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename) #Upload path staic/upload/filename.png
        #path_encryption="../assets/"
        file.save(full_filename)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        Kc,Kr,Iterations=encrypt_image(full_filename)
        parse_attributes_into_txt(Kc,Kr,Iterations)
        
        pathy="static/uploads/test1.png"
        return render_template('show.html',pathy=pathy,filename=filename, full_filename=full_filename,Kc=Kc,Kr=Kr,Iterations=Iterations)
        # return render_template('show.html',pathy=pathy,filename=filename, full_filename=full_filename)

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/decrypt_image')  #open the decrypt page and upload the 'shaky' pic to get clear pic 
def decrypt_image():
    render_template('decrypt.html')




def parse_attributes_into_txt(kc,kr,ITER_MAX): #take list as input

    with open('kc.txt', 'w') as filehandle:
        for listitem in kc:
            filehandle.write('%s\n' % listitem)

    with open('kr.txt', 'w') as filehandle:
        for listitem in kr:
            filehandle.write('%s\n' % listitem)
    
    with open('ITER_MAX.txt', 'w') as filehandle:
            filehandle.write(str(ITER_MAX))



def parse_txt_into_list(path_with_filename): #str input 
	#my_file = open(path_with_filename, "r")
	#content = my_file.read()
	pass



if __name__ == "__main__":
    app.run()
