import os
import pickle
from utils import *
from PIL import Image
import streamlit as st
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications.vgg16 import VGG16

img_model = VGG16()
img_model = Model(inputs = img_model.inputs, outputs = img_model.layers[-2].output)
model = load_model("Projects/imgcap/model")

with open("Projects/imgcap/tokenizer.pkl", "rb") as file: 
    tokenizer = pickle.load(file) 

def app() :
    st.title(":camera_with_flash::hash: ImgCap")
    st.text("Your uploaded image is")
    img = Image.open("image.jpg")
    st.image(img, width = 200)
    caption = generate_caption("image.jpg", img_model, model, tokenizer, 31)
    st.text("The generated caption is")
    st.caption(caption)

    if st.button("Upload another image") :
        os.remove("Projects/imgcap/image.jpg")
        st.rerun()
