import gspread
import attendance
import pandas as pd
import firebase_admin
import streamlit as st
from datetime import datetime
from firebase_admin import credentials, auth

if "verification_path" not in st.session_state:
    st.session_state.verification_path = "Projects/AttendanceSystem/input_image.jpg"

if "initiation_url" not in st.session_state:
    st.session_state.verification_url= "http://helpful-boxer-wrongly.ngrok-free.app/login"

if "verification_url" not in st.session_state:
    st.session_state.verification_url= "http://helpful-boxer-wrongly.ngrok-free.app/predict"

if "subject" not in st.session_state:
    st.session_state["subject"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "credentials" not in st.session_state:
    st.session_state.credentials = None

try:
    my_credentials = {
  "type": "service_account",
  "project_id": st.secrets["FIREBASE_PROJECT_ID"],
  "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
  "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
  "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
  "client_id": st.secrets["FIREBASE_CLIENT_ID"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": st.secrets["FIREBASE_CERT_URL"],
  "universe_domain": "googleapis.com"
}

    cred = credentials.Certificate(my_credentials)
    firebase_admin.initialize_app(cred)
except:
    pass

def app():
    st.title(":neutral_face::face_with_raised_eyebrow: Attendance System")

    email = st.text_input("Email :")
    password = st.text_input("Password :", type = "password")

    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email = email)

            if st.secrets[user.uid] != password:
                raise "Invalid Password"
            
            st.success(f"Login successful")
            timestamp = datetime.now()
            month = timestamp.strftime("%B")
            st.session_state["username"] = user.uid
            st.session_state["credentials"] = {
                "type": "service_account",
                "project_id": st.secrets["GSHEET_PROJECT_ID"],
                "private_key_id": st.secrets["GSHEET_PRIVATE_KEY_ID"],
                "private_key": st.secrets["GSHEET_PRIVATE_KEY"].replace("\\n", "\n"),
                "client_email": st.secrets["GSHEET_CLIENT_EMAIL"],
                "client_id": st.secrets["GSHEET_CLIENT_ID"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": st.secrets["GSHEET_CERT_URL"],
                "universe_domain": "googleapis.com"
            }
            gc = gspread.service_account_from_dict(st.session_state["credentials"])

            if st.session_state["username"] == "BkTK8QjyduRHYFABt39ev8f7Rae2":
                st.session_state["subject"] = "ANN"

            if st.session_state["username"] == "r19SGLazAkTOTuiozdDHWf9WQ0A3":
                st.session_state["subject"] = "DS"

            sh = gc.create(f"{month}'s Attendance For {st.session_state['subject']}")
            sh.share(st.secrets[f"{st.session_state['subject']}_EMAIL"], perm_type = "user", role = "writer")
            worksheet = sh.add_worksheet(title = timestamp.date(), rows = 100, cols  = 10)
            worksheet.append_row(["Roll No", "Name", "Time"])
            worksheet.format("A1:C1", {"textFormat": {"bold": True}})
            st.session_state["worksheet"] = worksheet
            st.session_state.runpage = attendance.app
            st.rerun()

        except Exception as e:
            st.warning(e)

if __name__ == "__main__":
    if "runpage" not in st.session_state:
        st.session_state.runpage = app
    st.session_state.runpage()