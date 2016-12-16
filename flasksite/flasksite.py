"""
    Small website for hosting the application.
"""
from flask import Flask, render_template
from keras.models import model_from_json
from keras import backend as K
from subprocess import call
import cv2
import numpy as np
from flask import request, url_for

app = Flask(__name__)


@app.route('/')
def hello_world(name=None):
    return render_template('index.html', gif="static/img/giphy.gif")

@app.route('/animate',methods=["GET","POST"])
def animate(name=None):
    #Test images
    #Save images from form to specific paths
    #print request.form["ImageURL1"]
    #print request.form["ImageURL2"]
    if request.method == "GET":
        gifLocation = "static/img/giphy.gif"
        return render_template('index.html', gif=gifLocation)
    if request.method == "POST":
        path = "./data/demo_images/"
        start_path = "{0}{1}".format(path, request.form['ImageURL1'])
        end_path = "{0}{1}".format(path, request.form['ImageURL2'])
        #start_path = "./data/0/6P1GwVf6B4D72_frames/frame0.jpg"
        #end_path = "./data/0/6P1GwVf6B4D72_frames/frame25.jpg"
        #Load and resize images
        start_img = cv2.imread(start_path)
        end_img = cv2.imread(end_path)

        #start_img = np.asarray([cv2.resize(start_img, (32, 32)).astype(np.float32)])
        #end_img = np.asarray([cv2.resize(end_img, (32,32)).astype(np.float32)])
        start_img = cv2.resize(start_img, (32, 32)).astype(np.float32)
        end_img = cv2.resize(end_img, (32, 32)).astype(np.float32)

        start_img = np.swapaxes(start_img, 0, 2)
        start_img = np.swapaxes(start_img, 1, 2)
        start_img = np.asarray([start_img])
        end_img = np.swapaxes(end_img, 0, 2)
        end_img = np.swapaxes(end_img, 1, 2)
        end_img = np.asarray([end_img])

        start_img /= 255
        end_img /= 255

        encoder_architecture = "./encoder_architecture.json"
        encoder_weights = "./encoder_weights.h5"
        encoder_values = "./encoded_features.txt"

        model = model_from_json(open(encoder_architecture, "r").read())
        model.load_weights(encoder_weights)

        #model.predict start and end
        model.layers = model.layers[:-2]
        model.compile('rmsprop', 'categorical_crossentropy')

        feature_output = K.function([model.layers[0].input, K.learning_phase()],\
                                    [model.layers[-2].output])
        #Might need to put each of these in their own list
        start_features = feature_output([start_img, 0])
        end_features = feature_output([end_img, 0])

        out_file = open(encoder_values, "w")
        #concatenate predictions 
        #Might not be concatenated correctly
        concatenated_features = list(np.concatenate((start_features[0][0], end_features[0][0]), axis=0))
        #write predictions out to encoder_values
        assert len(concatenated_features) == 100
        for f in range(0, len(concatenated_features)):
            #print f
            #out_file.write("{0}".format(concatenated_features[f]))
            if concatenated_features[f] == 0.0:
                concatenated_features[f] = np.random.normal(0, 1)
            if f == (len(concatenated_features) - 1):
                out_file.write("{0}".format(concatenated_features[f]))
            else:
                out_file.write("{0} ".format(concatenated_features[f]))
        out_file.close()

        #call th generate.lua
        call(["th", "./generate.lua"])
        #access generated gif location
        gifLocation = "static/img/gen.gif"
        #gifLocation = "static/img/giphy.gif"
        return render_template('index.html', gif=gifLocation)

if __name__ == "__main__":
    app.run()
