import requests
import streamlit as st
from datetime import datetime

def app():
    st.title(":neutral_face::face_with_raised_eyebrow: Attendance System")
    st.text("Let's mark your attendance for today")
    
    image = st.camera_input(label = "Take a good shot covering all of your face", help = "Avoid any masks, hats or any other occlusions", key = "verification_cam")

    if image :
        with open(st.session_state.verification_path, "wb") as file :
            file.write(image.getbuffer())
        
        image_file = open(st.session_state.verification_path, "rb")
        files = {"input_image": image_file}

        response = requests.post(st.session_state.verification_url, files = files)

        if response.status_code == 200:
            response_dict = response.json()  
            timestamp = datetime.now()
            time = timestamp.strftime("%I:%M %p")
            worksheet = st.session_state["worksheet"]
            worksheet.append_row([response_dict["rollno"], response_dict["name"], time])
            st.success(f"Hello { response_dict['name']}, your attendance has been recorded")
            st.rerun()
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            st.rerun()

    with st.sidebar():
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]    
            st.rerun()
