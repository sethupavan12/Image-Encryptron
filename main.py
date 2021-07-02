import os
from app import app

import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,session
from flask_wtf import Form
from wtforms import IntegerField, StringField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
from PIL import Image
from random import randint
import numpy
import sys
from helper import *
from encrypt import encrypt_image
from decrypt import decrypt_image

class InputForm(Form):
    Kc = IntegerField(label='Kc',validators=[DataRequired()])
    Kr = IntegerField(label='Kr',validators=[DataRequired()])
    ITER_MAX = IntegerField(label='ITER_MAX',validators=[DataRequired()])
    submit = SubmitField('Submit')



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
    form = InputForm()
    return render_template('decrypt.html',form=form)
    



@app.route('/decrypt_image',methods=['POST'])
def post_decrypt_image():
    if 'file' not in request.files:
        flash('No file found')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename) #Upload path decrypted_images/filename.png

        file.save(full_filename)
        #print('upload_image filename: ' + filename)

        form = InputForm()
        if form.validate_on_submit:
            #get values from a form
            Kc = request.form.getlist('Kc', type=int)
            Kr = request.form.getlist('Kr', type=int)
            ITER_MAX = request.form('ITER_MAX', type=int)


            decrypt_image(full_filename,Kc,Kr,ITER_MAX)
            flash('image decrypted')
            pathy='decrypted_images/decrypt.png'
            return render_template('decrypt.html',pathy=pathy,full_filename=full_filename,form=form)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)




def parse_attributes_into_txt(kc,kr,ITER_MAX): #take list as input

    with open('kc.txt', 'w') as filehandle:
        for listitem in kc:
            filehandle.write('%s\n' % listitem)

    with open('kr.txt', 'w') as filehandle:
        for listitem in kr:
            filehandle.write('%s\n' % listitem)
    
    with open('ITER_MAX.txt', 'w') as filehandle:
            filehandle.write(str(ITER_MAX))



def parse_txt_into_list(path_with_filename): #str input   #NO NEED TO USE NOW
    #my_file = open(path_with_filename, "r")
    content=[]
    with open(path_with_filename, 'r'):
        for i in path_with_filename:
            content.append(i)

    return content




if __name__ == "__main__":
    app.run()

#THINGS TO DO 
# ADD DOWNLOAD BUTTON FOR THE IMAGE