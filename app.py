from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import os
import threading

app = Flask(__name__)

model = tf.keras.models.load_model('./model/potato_disease_cnn_new')
clas_names = ["Early Blight", "Late Blight", "Healthy"]

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    imgfile = request.files['img_file']
    image_path = './static/images/'+imgfile.filename
    imgfile.save(image_path)
    img = load_img(image_path, target_size=(256,256))
    img = img_to_array(img)
    img_batch = np.expand_dims(img, 0)
 
    predictions = model.predict(img_batch)
    predicted_class = clas_names[np.argmax(predictions[0])]
    confidence = format(np.max(predictions[0])*100, ".2f")
   

    prstring = predicted_class+" with "+str(confidence)
    print(prstring)

    return render_template('prediction.html', data={"image":image_path, "prediction":predicted_class, "acuuracy":confidence})

# This is for Local Developement purpose 

# if __name__ == '__main__':
#     app.run(port=3000, debug=True)