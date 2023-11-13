import numpy as np
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def index_to_word(y, tokenizer) :
  for word, index in tokenizer.word_index.items():
    if index == y :
      return word
  return None

def predict_caption(model, image, tokenizer, max_length) :
  in_text = "start"
  for i in range(max_length) :
    sequence = tokenizer.texts_to_sequences([in_text])[0]
    sequence = pad_sequences([sequence], max_length)
    prediction = model.predict([image, sequence], verbose = 1)
    result = np.argmax(prediction)
    word = index_to_word(result, tokenizer)

    if word is None :
      break

    in_text += " " + word

    if word == "end" :
      break

  return in_text

def generate_caption(img_path, img_model, model, tokenizer, max_length) :
  img = load_img(img_path, target_size = (224, 224))
  img = img_to_array(img)
  img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
  img = preprocess_input(img)
  feature = img_model.predict(img, verbose = 0)
  y_pred = predict_caption(model, feature, tokenizer, max_length)
  return y_pred