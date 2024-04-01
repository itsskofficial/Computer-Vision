import os
import cv2
import streamlit as st

def detect_faces(image_path):
    faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
    )

    output_dir = "detected_faces"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
	
    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        resized_face = cv2.resize(face, (250, 250))
        face_filename = os.path.join(output_dir, f"face_{i+1}.jpg")
        cv2.imwrite(face_filename, resized_face)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
    cv2.imwrite(st.session_state["modified_image_path"], image)