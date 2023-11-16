import os
from utils import *
import streamlit as st
import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import BinaryCrossentropy

class L1Dist(Layer) :
  def __init__(self, **kwargs) :
    super().__init__()

  def call(self, input_embedding, validation_embedding) :
    return tf.math.abs(input_embedding -  validation_embedding)

model = load_model("Projects/facerec/model", custom_objects = {"L1Dist" : L1Dist, "BinaryCrossentropy" : BinaryCrossentropy})

def app() :
    st.title(":neutral_face::face_with_raised_eyebrow: FaceRec")
    st.text("Now let's capture the main image to verify whether its you or not")
    image = st.camera_input(label = "Take one good picture", help = "Make sure you are not wearing any specs or hats", key = "verification_cam")

    if image :
        with open(f"{st.session_state.input_path}/image.jpg", "wb") as file :
            file.write(image.getbuffer())
            verified = verify(model, 0.5, 0.7)
            if verified == True :
                st.write("You are verified")
            else :
                st.write("Sorry, its not you")

    if st.button("Do it again") :
        for root, dirs, files in os.walk(st.session_state.validation_path, topdown = False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

        for root, dirs, files in os.walk(st.session_state.input_path, topdown = False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        
        for key in st.session_state.keys():
                if key == "runpage" or key == "image_count" :
                    del st.session_state[key]  
        
        st.rerun()