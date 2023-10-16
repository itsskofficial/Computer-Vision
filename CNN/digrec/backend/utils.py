import urllib
import numpy as np
import cv2
import tensorflow as tf

def recognize(image):
    data = urllib.request.urlopen(image)
    with open('image.png', 'wb') as f:
        f.write(data.file.read())
    img = cv2.imread('image.png')[:,:,0]
    img = np.invert(np.array([img]))
    model = tf.keras.models.load_model('model')
    prediction = model.predict(img)
    return prediction