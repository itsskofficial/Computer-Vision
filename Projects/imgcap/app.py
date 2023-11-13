import caption
import streamlit as st

if "caption" not in st.session_state:
    st.session_state.caption = ""

if "image" not in st.session_state:
    st.session_state.image = None

def app():
    st.title("ImgCap")
    st.text("Upload any image below to generate a custom caption")
    image = st.file_uploader(label = "Only .jpg format supported", type = ["jpg"])
    st.session_state.image = image

    with open("image.jpg", "wb") as file :
        file.write(image.load_buffer())

    if st.button("Submit") :
        st.session_state.runpage = caption.app
        st.rerun()

if __name__ == "__app__":
    if "runpage" not in st.session_state:
        st.session_state.runpage = app
    st.session_state.runpage()