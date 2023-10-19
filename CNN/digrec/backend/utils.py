import urllib
import numpy as np
import cv2
import os
import tensorflow as tf

def recognize(dataURL):
    data = urllib.request.urlopen(dataURL).read()
    with open('image.png', 'wb') as f:
        f.write(data)
    img = cv2.imread('image.png')[:,:,0]
    img = np.array([img])
    img = np.reshape(img, (28, 28))
    img = np.invert(img)
    model = tf.keras.models.load_model('model')
    prediction = tf.argmax(model.predict(img), axis = 1)
    print(prediction)
    os.remove("image.png")
    return prediction