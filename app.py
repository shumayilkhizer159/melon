from flask import Flask,jsonify,request,render_template,Response,json
from keras.models import load_model
import cv2
import numpy as np
from tensorflow.python.lib.io import file_io
import os
from google.cloud import storage
app = Flask(__name__)
#MODEL_BUCKET = os.environ['melonomabucket']
#MODEL_FILENAME = os.environ['Melanoma95.h5']
#MODEL = None

@app.route('/')
def Homi():
    return "<h1>hello WORLD -- HOMEPAGE</h1>"
@app.route('/test/response')
def home():
    string = {"response":'Hello from tensorflow -- Usman Shakeel'}
    return string
@app.route('/api/test', methods=['POST'])
def test():
    try:
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # do some fancy processing here....
        img = img/255.0 #rescaling the between 0 - 1
        img = cv2.resize(img,(224,224)) 
        img = img.reshape(1,224,224,3)
        model_file = file_io.FileIO('gs://melonomabucket/Melanoma95.h5', mode='rb')
        temp_model_location = './temp_model.h5'
        temp_model_file = open(temp_model_location, 'wb')
        temp_model_file.write(model_file.read())
        temp_model_file.close()
        model_file.close()
        MODEL = load_model('./temp_model.h5')
        result = MODEL.predict_classes(img)
        #result = modeldata.predict_classes(img)
        # build a response dict to send back to client
        response = {'message': 'image received. size={}x{} Class = {}'.format(img.shape[1], img.shape[0],result[0])}
        # encode response using jsonpickle
        #response_pickled = jsonpickle.encode(response)
        #response_pickled = jsonify(response)
        #return Response(response=response_pickled, status=200, mimetype="application/json")

        response = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = {'message': 'ERROR OCCURED'}
        # encode response using jsonpickle
        #response_pickled = jsonpickle.encode(response)
        #response_pickled = jsonify(response)
        #return Response(response=response_pickled, status=200, mimetype="application/json")

        response = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
        return response
if __name__ == '__main__':
    app.run(port=8008)