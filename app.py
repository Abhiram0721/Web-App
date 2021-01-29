import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__) #Initialize the flask App
# model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('result.html')


@app.route('/in')
def home1():
    return render_template('in.html')


@app.route('/result',methods=['POST'])
def ValuePredictor():
    to_predict_list = request.form.to_dict()
    to_predict_list=list(to_predict_list.values())
    print(to_predict_list)
    to_predict_list = list(map(int, to_predict_list))
    to_predict = np.array(to_predict_list).reshape(1,11)
    # loaded_model = pickle.load(open("model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    if int(result)==0:
        prediction='Andrea'
    elif int(result)==1:
        prediction='Alexandra'
    elif int(result)==2:
        prediction='Melisha'
    elif int(result)==3:
        prediction='Botez'
    else:
        prediction='Kacey'
    return render_template("result.html",prediction=prediction)
    
if __name__ == "__main__":
    app.run(debug=True, port = 80)