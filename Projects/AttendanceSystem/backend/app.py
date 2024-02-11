import os
import json
import urllib
import uvicorn
import numpy as np
import nest_asyncio
import tensorflow as tf
from pyngrok import ngrok
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ngrok.set_auth_token("2WfNAfRBJZK6oe2x0Sl9QVRl5Zv_5wxr2UnS1CBuJmycrFk2k")

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class L1Dist(tf.keras.layers.Layer):

    def __init__(self, **kwargs):
        super().__init__()

    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)

class Face(BaseModel):
    image: str

verified_students = None
model = tf.keras.models.load_model("siamesemodel_4_classes.h5",
                                    custom_objects = {"L1Dist" : L1Dist, "BinaryCrossentropy" : tf.losses.BinaryCrossentropy})

def preprocess(file_path):
    byte_img = tf.io.read_file(file_path)
    img = tf.io.decode_jpeg(byte_img)
    img = tf.image.resize(img, (100,100))
    img = img / 255.0

    return img

def get_prediction():
    results = []
    count = 0
    verified_id = None
    max_probability = 0
    global verified_students
    global model

    for f in os.listdir("application_data") and f not in verified_students:
        if os.path.isfile(os.path.join("application_data", f)):
            continue
        else:
            results.append({
                "id" : f,
                "probability" : None,
            })

            for image in os.listdir(os.path.join("application_data", f, "verification_images")):
                input_img = preprocess(os.path.join("application_data", "input_image.jpg"))
                validation_img = preprocess(os.path.join("application_data", f, "verification_images", image))
                input_img = np.expand_dims(input_img, axis = 0)
                validation_img = np.expand_dims(validation_img, axis = 0)
                result = model.predict([input_img, validation_img])
                results[count]["probability"] = result

                if result > max_probability:
                    max_probability = result
                    verified_id = f

            print(results[count])
            count += 1

    if verified_id != None:
        info_path = os.path.join("application_data", verified_id, "info.json")
        verified_students.append(verified_id)

        with open(info_path) as f:
            info = json.load(f)

        print(info)
        return info

    return None

@app.get("/")
def home():
    return {"message" : "Hey there. Please send a POST request to /predict with your image to mark your attendance"}

@app.post("/initiate", status_code = 200)
def initiate():
    try:
        global verified_students
        verified_students = []
        return {"message": "success"}

    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.post("/predict", status_code = 200)
def predict(image: Face):
    try:
        dataURL = image.input_image
        data = urllib.request.urlopen(dataURL).read()

        with open("application_data/input_image.jpg", "wb") as f:
            f.write(data)

        result = get_prediction()
        return result

    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

ngrok_tunnel = ngrok.connect(addr = 8000, domain = "helpful-boxer-wrongly.ngrok-free.app")
print("Public URL: ", ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port = 8000)