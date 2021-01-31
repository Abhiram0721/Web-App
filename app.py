from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os, shutil
import easyocr
from textblob import TextBlob
import numpy as np
import keras
from tensorflow.keras.preprocessing.image import load_img 
from tensorflow.keras.applications.xception import preprocess_input


UPLOAD_FOLDER = "static/img"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




model = keras.models.load_model('model1.h5')
reader = easyocr.Reader(["en"])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home')
def home1():
    return render_template('index.html')


@app.route('/result',methods=['GET', 'POST'])
def homeUp():

  if request.method == 'POST':
        # check if the post request has the file part
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['img']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
            print(filename)

  image_size = (299, 299)

  labels = {0:'dress', 1:'hat', 2:'longsleeve', 3:'outwear', 4:'jeans',
           5:'shirt', 6:'shoes', 7:'shorts',  8:'skirt', 9:'t-shirt'}

  image = (os.listdir("static/img"))
  img = load_img("static/img/" + image[0], target_size=(image_size))
  x = np.array(img)
  X = np.array([x])
  X = preprocess_input(X)
  pred = model.predict(X)
  prediction = labels[pred[0].argmax()]

  
  folder = UPLOAD_FOLDER
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

  return render_template('product_layout.html',prediction=prediction)






@app.route('/senti',methods=['POST'])
def senti():

  to_predict_list = request.form.to_dict()
  to_predict_list=list(to_predict_list.values())
  feedback = ' '.join( to_predict_list ) 

  polarity = 0

  analysis = TextBlob(feedback)
  polarity = polarity + analysis.sentiment.polarity

  if (analysis.sentiment.polarity == 0.00):
    feed = "Sorry, we will improve our Service."

  elif (analysis.sentiment.polarity > 0.00):
    feed = "Thanks for Appreciating our Service."

  elif (analysis.sentiment.polarity < 0.00):
    feed = "Sorry, we will improve our Service."

  prediction = feed

  return render_template("senti_result.html",prediction=prediction, feedback=feedback)

    

@app.route('/coupon',methods=['GET', 'POST'])
def coupan():
  
  if request.method == 'POST':
        # check if the post request has the file part
        if 'img_coupon' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['img_coupon']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
            print(filename)

  image = (os.listdir("static/img"))
  img_path = "static/img/" + image[0]
  res = reader.readtext(img_path)

  ls=[]
  for i in res:
    j = i[1]
    ls.append(j)

  prediction = ' '.join(ls) 
  prediction

  
  folder = UPLOAD_FOLDER
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

  return render_template('coupon.html',prediction=prediction)





if __name__ == "__main__":
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run()