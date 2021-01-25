from flask import Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
import time
import os
import easyocr
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = "E:\\Aarush\\Project\\Standalone\\app\\uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSH_BASE'] = "whoosh"

db = SQLAlchemy(app)

class Records(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(500), nullable=False, unique=True)
    text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.filepath}', '{self.text}')"


def add_image(filename, final):
    image = Records(
        filepath = filename,
        text = final
    )
    
    db.session.add(image)
    db.session.commit()

@app.route('/upload-image', methods=['GET','POST'])
def upload_image():
    
    if request.method=='POST':
        if request.files:
            image=request.files['image']
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            
            filename = image.filename.split('.')[0] + str(time.time()) + "." + image.filename.split('.')[1]

            image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
            print("Image saved")
            
            

            
            reader = easyocr.Reader(['en']) # need to run only once to load model into memory
            
            fp = 'uploads\\' + filename
            result = reader.readtext(fp, detail=0)
            final = ",".join(result)
            

            image = Records(filepath = filename,text = final)
                    
            db.session.add(image)
            db.session.commit()           

    return render_template('upload_image.html')

@app.route('/search')
def search_keyword():
    if request.method=='GET':
        r = Records.query.all()


    return render_template('search.html')

@app.route('/records')
def download():
    return render_template('records.html')
