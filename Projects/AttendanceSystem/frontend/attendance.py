import os
import cv2
import json
import base64
import requests
from utils import *
from gtts import gTTS
import soundfile as sf
import streamlit as st
import sounddevice as sd
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
from unittest.mock import Mock

load_dotenv("secrets.env")
client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def text_to_speech(text, output_file = "greeting.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

def play_audio(file_path):
    data, fs = sf.read(file_path, dtype = "float32")
    sd.play(data, fs)
    sd.wait()

def app():
    st.title(":neutral_face::face_with_raised_eyebrow: Attendance System")
    st.text("Let's mark your attendance for today")
    with st.sidebar:
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]   
            st.rerun()
    
    cap = cv2.VideoCapture(1)
    frame_placeholder = st.empty()

    capture_button = st.button("Capture") 

    while not capture_button:
        ret, frame = cap.read()
        st.session_state["image"] = frame
        frame_placeholder.image(st.session_state["image"], channels = "BGR")

    frame_placeholder.image(st.session_state["image"], channels = "BGR")

    cv2.imwrite(st.session_state["input_image_path"], st.session_state["image"])

    cap.release()
    cv2.destroyAllWindows() 

    try:
        verified_students = 0
        detect_faces(st.session_state["input_image_path"])

        for face in os.listdir("detected_faces"):
            with open(os.path.join("detected_faces", face), "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            
            data = {"image": encoded_image}
            headers = {"Content-Type": "application/json"}
            json_data = json.dumps(data)
            # dummy_json_response = Mock()
            # dummy_json_response.status_code = 200
            # dummy_json_response.json.return_value = {"rollno": "8001", "name": "Sarthak Karandikar"}
            
            # response = dummy_json_response
            response = requests.post(st.session_state["verification_url"], data = json_data, headers = headers)

            if response.status_code == 200:
                response_dict = response.json()  
                timestamp = datetime.now()
                time = timestamp.strftime("%I:%M %p")
                worksheet = st.session_state["worksheet"]
                worksheet.append_row([response_dict["rollno"], response_dict["name"], time])
                verified_students += 1
            else:
                response_dict = response.json()
                raise Exception(response_dict["detail"])

        client.messages.create(
        to = os.environ[f"{st.session_state['subject']}_NO"],
        from_ = os.environ["TWILIO_NO"],
        body = f"Attendance marked of {verified_students} students"
    )
            
        for face in os.listdir("detected_faces"):
            os.remove(os.path.join("detected_faces", face))

    except Exception as e:
        if e == "'NoneType' object is not subscriptable":
            st.error("No person verified")
            for face in os.listdir("detected_faces"):
                os.remove(os.path.join("detected_faces", face))
        else:
            st.error(e)
            for face in os.listdir("detected_faces"):
                os.remove(os.path.join("detected_faces", face))
    
    finally:
        st.rerun()

    