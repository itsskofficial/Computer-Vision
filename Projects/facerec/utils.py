import os
import numpy as np
from utils import *
import streamlit as st
import tensorflow as tf

def verify(model, detection_threshold, verification_threshold) :
  results = []
  for image in os.listdir(st.session_state.validation_path) :
    input_img = preprocess(os.path.join(st.session_state.input_path, "image.jpg"))
    validation_img = preprocess(os.path.join(st.session_state.validation_path, image))
    result = model.predict(list(np.expand_dims([input_img, validation_img], axis = 1)))
    results.append(result)
    print(results)

  detection = np.sum(np.array(results) > detection_threshold)
  verification = detection / len(os.listdir(os.path.join(st.session_state.validation_path)))
  verified = verification > verification_threshold

  return verified

def preprocess(file_path) :
  byte_img = tf.io.read_file(file_path)
  img = tf.io.decode_jpeg(byte_img)
  img = tf.image.resize(img, (100, 100))
  img = img / 255.0

  return img

