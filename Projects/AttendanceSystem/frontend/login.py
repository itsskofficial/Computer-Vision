import os
import gspread
import requests
import attendance
import firebase_admin
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from firebase_admin import credentials, auth

load_dotenv("secrets.env")

if "verification_path" not in st.session_state:
    st.session_state["verification_path"] = "./input_image.jpg"

if "initiation_url" not in st.session_state:
    st.session_state["initiation_url"]= "https://helpful-boxer-wrongly.ngrok-free.app/initiate"

if "verification_url" not in st.session_state:
    st.session_state["verification_url"]= "https://helpful-boxer-wrongly.ngrok-free.app/predict"

if "subject" not in st.session_state:
    st.session_state["subject"] = None

if "image" not in st.session_state:
    st.session_state["image"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "gsheet_credentials" not in st.session_state:
    st.session_state["gsheet_credentials"] = None

try:
    my_credentials = {
  "type": "service_account",
  "project_id": os.environ["FIREBASE_PROJECT_ID"],
  "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
  "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
  "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
  "client_id": os.environ["FIREBASE_CLIENT_ID"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ["FIREBASE_CERT_URL"],
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

            if os.environ[user.uid] != password:
                raise Exception("Invalid Password")
            
            timestamp = datetime.now()
            month = timestamp.strftime("%B")
            st.session_state["username"] = user.uid
            st.session_state["gsheet_credentials"] = {
                "type": "service_account",
                "project_id": os.environ["GSHEET_PROJECT_ID"],
                "private_key_id": os.environ["GSHEET_PRIVATE_KEY_ID"],
                "private_key": os.environ["GSHEET_PRIVATE_KEY"].replace("\\n", "\n"),
                "client_email": os.environ["GSHEET_CLIENT_EMAIL"],
                "client_id": os.environ["GSHEET_CLIENT_ID"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.environ["GSHEET_CERT_URL"],
                "universe_domain": "googleapis.com"
            }

            gc = gspread.service_account_from_dict(st.session_state["gsheet_credentials"])

            if st.session_state["username"] == "BkTK8QjyduRHYFABt39ev8f7Rae2":
                st.session_state["subject"] = "ANN"

            if st.session_state["username"] == "r19SGLazAkTOTuiozdDHWf9WQ0A3":
                st.session_state["subject"] = "DS"

            spreadsheet_title = f"{month}'s Attendance For {st.session_state['subject']}"

            try:
                sh = gc.open(spreadsheet_title)
            except gspread.exceptions.SpreadsheetNotFound:
                sh = gc.create(spreadsheet_title)
                sh.share(os.environ[f"{st.session_state['subject']}_EMAIL"], perm_type = "user", role = "writer")
            
            worksheet_title = timestamp.strftime("%Y-%m-%d")
            
            try:
                worksheet = sh.worksheet(worksheet_title)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sh.add_worksheet(title=worksheet_title, rows="100", cols="20") 
                worksheet.append_row(["Roll No", "Name", "Time"])
                worksheet.format("A1:C1", {"textFormat": {"bold": True}})

            st.session_state["worksheet"] = worksheet
            
            response = requests.post(st.session_state["initiation_url"])

            if response.status_code == 200:
                st.success(f"Login successful")
                st.session_state.runpage = attendance.app
                st.rerun()
            else:
                response_dict = response.json()
                raise Exception(response_dict["detail"])
            
        except Exception as e:
            st.error(e)

if __name__ == "__main__":
    if "runpage" not in st.session_state:
        st.session_state.runpage = app
    st.session_state.runpage()