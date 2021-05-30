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
        
        
		pathy="static/uploads/test1.png"
		return render_template('show.html',pathy=pathy,filename=filename, full_filename=full_filename,Kc=Kc,Kr=Kr,Iterations=Iterations)
		# return render_template('show.html',pathy=pathy,filename=filename, full_filename=full_filename)

	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

#@app.route('/display/<filename>')
#def display_image(filename):
	#print('display_image filename: ' + filename)
	#return redirect(url_for('static', filename='uploads/' + filename), code=301)
	#return render_template('show.html')



# def encrypt_image(full_filename,filename):
	# im = Image.open(full_filename)
	# pix = im.load()
	# # Obtaining the RGB matrices
	# r = []
	# g = []
	# b = []
	# for i in range(im.size[0]):
	# 	r.append([])
	# 	g.append([])
	# 	b.append([]) 
	# 	for j in range(im.size[1]):
	# 		rgbPerPixel = pix[i,j]
	# 		r[i].append(rgbPerPixel[0])
	# 		g[i].append(rgbPerPixel[1])
	# 		b[i].append(rgbPerPixel[2])

	# m = im.size[0]
	# n = im.size[1]

	# # Vectors Kr and Kc
	# alpha = 8
	# Kr = [randint(0,pow(2,alpha)-1) for i in range(m)]
	# Kc = [randint(0,pow(2,alpha)-1) for i in range(n)]
	# ITER_MAX = 1

	# print('Vector Kr : ', Kr)
	# print('Vector Kc : ', Kc)

	# f = open('keys.txt','w+')
	# f.write('Vector Kr : \n')
	# for a in Kr:
	# 	f.write(str(a) + '\n')
	# f.write('Vector Kc : \n')
	# for a in Kc:
	# 	f.write(str(a) + '\n')
	# f.write('ITER_MAX : \n')
	# f.write(str(ITER_MAX) + '\n')


	# for iterations in range(ITER_MAX):
	# 	# For each row
	# 	for i in range(m):
	# 		rTotalSum = sum(r[i])
	# 		gTotalSum = sum(g[i])
	# 		bTotalSum = sum(b[i])
	# 		rModulus = rTotalSum % 2
	# 		gModulus = gTotalSum % 2
	# 		bModulus = bTotalSum % 2
	# 		if(rModulus==0):
	# 			r[i] = numpy.roll(r[i],Kr[i])
	# 		else:
	# 			r[i] = numpy.roll(r[i],-Kr[i])
	# 		if(gModulus==0):
	# 			g[i] = numpy.roll(g[i],Kr[i])
	# 		else:
	# 			g[i] = numpy.roll(g[i],-Kr[i])
	# 		if(bModulus==0):
	# 			b[i] = numpy.roll(b[i],Kr[i])
	# 		else:
	# 			b[i] = numpy.roll(b[i],-Kr[i])
	# 	# For each column
	# 	for i in range(n):
	# 		rTotalSum = 0
	# 		gTotalSum = 0
	# 		bTotalSum = 0
	# 		for j in range(m):
	# 			rTotalSum += r[j][i]
	# 			gTotalSum += g[j][i]
	# 			bTotalSum += b[j][i]
	# 		rModulus = rTotalSum % 2
	# 		gModulus = gTotalSum % 2
	# 		bModulus = bTotalSum % 2
	# 		if(rModulus==0):
	# 			upshift(r,i,Kc[i])
	# 		else:
	# 			downshift(r,i,Kc[i])
	# 		if(gModulus==0):
	# 			upshift(g,i,Kc[i])
	# 		else:
	# 			downshift(g,i,Kc[i])
	# 		if(bModulus==0):
	# 			upshift(b,i,Kc[i])
	# 		else:
	# 			downshift(b,i,Kc[i])
	# 	# For each row
	# 	for i in range(m):
	# 		for j in range(n):
	# 			if(i%2==1):
	# 				r[i][j] = r[i][j] ^ Kc[j]
	# 				g[i][j] = g[i][j] ^ Kc[j]
	# 				b[i][j] = b[i][j] ^ Kc[j]
	# 			else:
	# 				r[i][j] = r[i][j] ^ rotate180(Kc[j])
	# 				g[i][j] = g[i][j] ^ rotate180(Kc[j])
	# 				b[i][j] = b[i][j] ^ rotate180(Kc[j])
	# 	# For each column
	# 	for j in range(n):
	# 		for i in range(m):
	# 			if(j%2==0):
	# 				r[i][j] = r[i][j] ^ Kr[i]
	# 				g[i][j] = g[i][j] ^ Kr[i]
	# 				b[i][j] = b[i][j] ^ Kr[i]
	# 			else:
	# 				r[i][j] = r[i][j] ^ rotate180(Kr[i])
	# 				g[i][j] = g[i][j] ^ rotate180(Kr[i])
	# 				b[i][j] = b[i][j] ^ rotate180(Kr[i])


	# for i in range(m):
	# 	for j in range(n):
	# 		pix[i,j] = (r[i][j],g[i][j],b[i][j])

    # # im.save('encrypted_images' + 'test1.png')
    # return Kr,Kc,ITER_MAX





if __name__ == "__main__":
    app.run()
