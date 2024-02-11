import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def preprocess(file_path):
    
    byte_img = tf.io.read_file(file_path)
    img = tf.io.decode_jpeg(byte_img)
    
    img = tf.image.resize(img, (100,100))
    img = img / 255.0
    
    return img

def preprocess_twin(input_img, validation_img, label):
    return(preprocess(input_img), preprocess(validation_img), label)

class L1Dist(tf.keras.layers.Layer):
    
    def __init__(self, **kwargs):
        super().__init__()
       
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)

base_path = '/content/data'

for roll_no in os.listdir(base_path):
    roll_no_path = os.path.join(base_path, roll_no)

    if os.path.isdir(roll_no_path):
        for pos_neg_anc in os.listdir(roll_no_path):
            pos_neg_anc_path = os.path.join(roll_no_path, pos_neg_anc)

            if pos_neg_anc == "positive":
                exec(f"POS{roll_no}_PATH = os.path.join('data', '{roll_no}', 'positive')")
            elif pos_neg_anc == "negative":
                exec(f"NEG{roll_no}_PATH = os.path.join('data', '{roll_no}', 'negative')")
            else:
                exec(f"ANC{roll_no}_PATH = os.path.join('data', '{roll_no}', 'anchor')")

for roll_no in os.listdir(base_path):
    exec(f"pattern_lower{roll_no} = NEG{roll_no}_PATH + '/*.jpg'")
    exec(f"pattern_upper{roll_no} = NEG{roll_no}_PATH + '/*.JPG'")
    
    exec(f"files_lower{roll_no} = tf.data.Dataset.list_files(pattern_lower{roll_no}).take(200)")
    exec(f"files_upper{roll_no} = tf.data.Dataset.list_files(pattern_upper{roll_no}).take(200)")

for roll_no in os.listdir(base_path):
    exec(f"anchor{roll_no} = tf.data.Dataset.list_files(ANC{roll_no}_PATH+'/*.jpg').take(200)")
    exec(f"positive{roll_no} = tf.data.Dataset.list_files(POS{roll_no}_PATH+'/*.jpg').take(200)")
    exec(f"negative{roll_no} = files_lower{roll_no}.concatenate(files_upper{roll_no})")

for roll_no in os.listdir(base_path):
    exec(f"positives{roll_no} = tf.data.Dataset.zip((anchor{roll_no}, positive{roll_no}, tf.data.Dataset.from_tensor_slices(tf       .ones(len(anchor{roll_no})))))")
    exec(f"negatives{roll_no} = tf.data.Dataset.zip((anchor{roll_no}, negative{roll_no}, tf.data.Dataset.from_tensor_slices(tf       .zeros(len(anchor{roll_no})))))")

data = None
for roll_no in os.listdir(base_path):
    if data == None:
        data = eval(f"positives{roll_no}.concatenate(negatives{roll_no})")
    else:
        data = eval(f"data.concatenate(positives{roll_no}).concatenate(negatives{roll_no})")

data = data.map(preprocess_twin)
data = data.cache()
data = data.shuffle(buffer_size=1024)

train_data = data.take(round(len(data)*.7))
train_data = train_data.batch(16)
train_data = train_data.prefetch(8)

test_data = data.skip(round(len(data)*.7))
test_data = test_data.take(round(len(data)*.3))
test_data = test_data.batch(16)
test_data = test_data.prefetch(8)

siamese_model = tf.keras.models.load_model('siamesemodel.h5', 
                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})

for i in range(15) :
  test_input, test_val, y_true = test_data.as_numpy_iterator().next()
  print(test_input.shape, test_val.shape)

  y_hat = siamese_model.predict([test_input, test_val])
  predictions = [1 if prediction > 0.5 else 0 for prediction in y_hat ]
  print(predictions)

  print("\n")

  print(y_true)

  plt.figure(figsize=(10,8))

  plt.subplot(1,2,1)
  plt.imshow(test_input[0])

  plt.subplot(1,2,2)
  plt.imshow(test_val[0])

  plt.show()
  print("\n\n\n")