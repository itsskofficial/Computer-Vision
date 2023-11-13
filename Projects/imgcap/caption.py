import os
import pickle
from utils import *
from PIL import Image
import streamlit as st
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications.vgg16 import VGG16

img_model = VGG16()
img_model = Model(inputs = img_model.inputs, outputs = img_model.layers[-2].output)

def app() :
    model = load_model("model")

    with open("tokenizer.pkl", "rb") as file: 
        tokenizer = pickle.load(file) 
    
    img = Image.open("image.jpg")
    st.image(img, width = 200)
    caption = generate_caption("image.jpg", img_model, model, tokenizer, 31)
    st.text(caption)

    if st.button("Upload another image") :
        os.remove("image.jpg")

        for key in st.session_state.keys() :
            del st.session_state[key]  

        st.rerun()
