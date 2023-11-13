import os
import pickle
from utils import *
from PIL import Image
import streamlit as st
from tensorflow.keras.models import load_model

def app() :
    model = load_model("model")
    img_model = load_model("img_model")

    with open("tokenizer.pkl", "rb") as file: 
        tokenizer = pickle.load(file) 
  
    img = Image.open("image.jpg")
    st.image(img)
    caption = generate_caption("image.jpg", img_model, model, tokenizer, 31)
    st.write(caption)
    if st.button("Upload another image") :
        os.remove("image.jpg")

        for key in st.session_state.keys() :
            del st.session_state[key]  

        st.rerun()
