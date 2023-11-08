import streamlit as st

if "caption" not in st.session_state:
    st.session_state.caption = ""

if "image" not in st.session_state:
    st.session_state.image = None

if "runpage" not in st.session_state:
    st.session_state.runpage = None

def app():
    st.title("ImgCap")
    st.text("Upload any image below to generate a custom caption")
    image = st.file_uploader(label = "Only .png & .jpg format supported", type = ["png", "jpg"])
    st.session_state.image = image