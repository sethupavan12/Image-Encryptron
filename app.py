from flask import Flask
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = 'decrypted_images/'
