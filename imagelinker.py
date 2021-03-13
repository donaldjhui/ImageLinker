import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import timedelta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

database = mongo.db.database


@app.route('/')
def index():
    saved_images = database.find()
    return render_template('index.html', images=saved_images)


@app.route('/upload/', methods=['POST'])
def upload():
    image_name = request.form.get('name')
    image_date = request.form.get('date')
    image_link = request.form.get('link')
    database.insert_one({
        'name': image_name,
        'date': image_date,
        'link': image_link
    })
    return redirect(url_for('index'))


@app.route('/search/', methods=['POST'])
def search():
    image_name = request.form.get('name')
    saved_images = database.find({
        'name': image_name
    })
    return render_template('search.html', images=saved_images, name=image_name)


if __name__ == '__main__':
    app.run(debug=True)
