import os
import uuid
import verification
import streamlit as st
import tensorflow as tf

if os.path.exists("Projects/facerec/data") ==  False:
    os.mkdir("Projects/facerec/data")

if "validation_path" not in st.session_state :
    st.session_state.validation_path = "Projects/facerec/data/validation"

if "input_path" not in st.session_state :
    st.session_state.input_path = "Projects/facerec/data/input"

if "image_count" not in st.session_state :
    st.session_state.image_count = 0

if os.path.exists("Projects/facerec/data/validation") ==  False:
    os.mkdir(st.session_state.validation_path)

if os.path.exists("Projects/facerec/data/input") ==  False:
    os.mkdir(st.session_state.input_path)



def app():
    st.title(":neutral_face::face_with_raised_eyebrow: FaceRec")
    st.text("First let's capture some images. Be sure to remove any specs or hats")
    

    image = st.camera_input(label = "Take at least 15 pictures for good results", help = "Pose differently for each image", key = "validation_cam")

    if image :
        with open(f"{st.session_state.validation_path}/{uuid.uuid1()}.jpg", "wb") as file :
            file.write(image.getbuffer())
            st.session_state.image_count += 1
            st.write(f"Pictures taken : {st.session_state.image_count}")
            

    if st.session_state.image_count >= 15 :
        st.write("Okay, we can proceed now")

        if st.button("Proceed") :
            st.session_state.runpage = verification.app
            st.rerun()

if __name__ == "__main__":
    if "runpage" not in st.session_state:
        st.session_state.runpage = app
    st.session_state.runpage()