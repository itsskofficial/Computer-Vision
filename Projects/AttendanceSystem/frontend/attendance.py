import os
import cv2
import json
import base64
import requests
from gtts import gTTS
import soundfile as sf
import streamlit as st
import sounddevice as sd
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

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
    
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()

    capture_button = st.button("Capture") 

    while not capture_button:
        ret, frame = cap.read()
        st.session_state["image"] = frame[120:120 + 450, 200: 200 + 350:]
        frame_placeholder.image(st.session_state["image"], channels = "BGR")

    frame_placeholder.image(st.session_state["image"], channels = "BGR")

    cv2.imwrite(st.session_state["verification_path"], st.session_state["image"])

    cap.release()
    cv2.destroyAllWindows() 

    try:        
        with open(st.session_state["verification_path"], "rb") as image_file:
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
            st.success(f"Hello { response_dict['name']}, your attendance has been recorded")
            greeting_text = f"Hello, {response_dict['name']}!"
            text_to_speech(greeting_text)
            play_audio("greeting.mp3")

            client.messages.create(
            to = os.environ[f"{st.session_state['subject']}_NO"],
            from_ = os.environ["TWILIO_NO"],
            body = f"Attendance Marked\nRollNo: {response_dict['rollno']}\nName: {response_dict['name']}"
        )
            
        else:
            response_dict = response.json()
            raise Exception(response_dict["detail"])
    
    except Exception as e:
        if e == "'NoneType' object is not subscriptable":
            st.error("No person verified")
        else:
            st.error(e)
    
    finally:
        st.rerun()

    