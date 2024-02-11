import os
import uuid
import random
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer, Conv2D, Dense, Dropout, MaxPooling2D, Input, Flatten, BatchNormalization

def preprocess(file_path):
    
    byte_img = tf.io.read_file(file_path)
    img = tf.io.decode_jpeg(byte_img)
    
    img = tf.image.resize(img, (100,100))
    img = img / 255.0
    
    return img

def preprocess_twin(input_img, validation_img, label):
    return(preprocess(input_img), preprocess(validation_img), label)

def make_embedding(): 
    inp = Input(shape=(100, 100, 3), name='input_image')
    
    c1 = Conv2D(64, (15, 15), activation='relu')(inp)
    c1 = BatchNormalization()(c1)
    m1 = MaxPooling2D((2, 2), padding='same')(c1)
    
    c2 = Conv2D(256, (7, 7), activation='relu')(m1)
    c2 = BatchNormalization()(c2)
    m2 = MaxPooling2D((2, 2), padding='same')(c2)
    
    c3 = Conv2D(256, (4, 4), activation='relu')(m2)
    c3 = BatchNormalization()(c3)
    m3 = MaxPooling2D((2, 2), padding='same')(c3)
    
    c4 = Conv2D(512, (4, 4), activation='relu')(m3)
    c4 = BatchNormalization()(c4)
    
    f1 = Flatten()(c4)
    d1 = Dense(1024, activation='sigmoid')(f1)
    
    return Model(inputs=[inp], outputs=[d1], name='embedding')

class L1Dist(Layer):
    
    def __init__(self, **kwargs):
        super().__init__()
       
    def call(self, input_embedding, validation_embedding):
        
        return tf.math.abs(input_embedding - validation_embedding)

def make_siamese_model(): 
    
    input_image = Input(name='input_img', shape=(100,100,3))
    
    validation_image = Input(name='validation_img', shape=(100,100,3))
    
    siamese_layer = L1Dist()
    siamese_layer._name = 'distance'
    distances = siamese_layer(embedding(input_image), embedding(validation_image))
    
    classifier = Dense(1, activation='sigmoid')(distances)
    
    return Model(inputs=[input_image, validation_image], outputs=classifier, name='SiameseNetwork')

@tf.function
def train_step(batch):
    
    with tf.GradientTape() as tape:     
        X = batch[:2]
        y = batch[2]
        
        yhat = siamese_model(X, training=True)
        loss = binary_cross_loss(y, yhat)
        binary_accuracy_metric.update_state(y, yhat)
        
    grad = tape.gradient(loss, siamese_model.trainable_variables)
    
    opt.apply_gradients(zip(grad, siamese_model.trainable_variables))
    accuracy = binary_accuracy_metric.result()
    binary_accuracy_metric.reset_states()
    
    return loss, accuracy

def train(data, EPOCHS):
    for epoch in range(1, EPOCHS+1):
        print('\n Epoch {}/{}'.format(epoch, EPOCHS))
        progbar = tf.keras.utils.Progbar(len(data))
        
        for idx, batch in enumerate(data):
            loss, accuracy = train_step(batch)
            progbar.update(idx+1, [('loss', loss), ('accuracy', accuracy)])
        
        if epoch % 10 == 0: 
            checkpoint.save(file_prefix=checkpoint_prefix)


gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus: 
    tf.config.experimental.set_memory_growth(gpu, True)

binary_accuracy_metric = tf.keras.metrics.BinaryAccuracy()

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

embedding = make_embedding()
l1 = L1Dist()
siamese_model = make_siamese_model()
binary_cross_loss = tf.losses.BinaryCrossentropy()
opt = tf.keras.optimizers.Adam(1e-3) 

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, 'ckpt')
checkpoint = tf.train.Checkpoint(opt=opt, siamese_model=siamese_model)

EPOCHS = 25
train(train_data, EPOCHS)

siamese_model.save('siamesemodel.h5')