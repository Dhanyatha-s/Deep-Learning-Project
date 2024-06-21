import os
import pathlib
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
tf.random.set_seed(42)

from PIL import Image, ImageOps
from IPython.display import display
import warnings
warnings.filterwarnings('ignore')
img1 = Image.open('./dataset/train/healthy/img2434.jpg')
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255.0)

train_data = train_datagen.flow_from_directory(
    directory='./dataset/train',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=64,
    seed=42
)

first_batch = train_data.next()
print(first_batch[0].shape), print(first_batch[1].shape)

def visualize_batch(batch: tf.keras.preprocessing.image.DirectoryIterator):
    n = 64
    num_row, num_col = 8, 8
    fig, axes = plt.subplots(num_row, num_col, figsize=(3 * num_col, 3 * num_row))
    
    for i in range(n):
        img = np.array(batch[0][i] * 255, dtype='uint8')
        ax = axes[i // num_col, i % num_col]
        ax.imshow(img)
        
    plt.tight_layout()
    plt.show()

valid_data = valid_datagen.flow_from_directory(
    directory='./dataset/val/',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=64,
    seed=42
)
model_1 = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=16, kernel_size=(3, 3), input_shape=(224, 224, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2), padding='same'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model_1.compile(
    loss=tf.keras.losses.categorical_crossentropy,
    optimizer=tf.keras.optimizers.Adam(),
    metrics=[tf.keras.metrics.BinaryAccuracy(name='accuracy')]
)

history_1 = model_1.fit(
    train_data,
    epochs=10,
    validation_data=valid_data

)

    
num_of_test_samples=len(valid_data.classes)
y_test=valid_data.classes
Y_pred = model_1.predict_generator(valid_data)
y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
from sklearn.metrics import precision_score, recall_score, f1_score,accuracy_score,confusion_matrix
print("confusion_matrix\n",confusion_matrix(valid_data.classes, y_pred))
print("Recall_score",recall_score(valid_data.classes, y_pred, pos_label='positive',average='micro'))
print("F1_score",f1_score(valid_data.classes, y_pred, pos_label='positive',average='micro'))
print("Precision_score",precision_score(valid_data.classes, y_pred, pos_label='positive',average='micro'))

import h5py
model_1.save('model_cnn1.h5')
import matplotlib.pyplot as plt
# summarize history for accuracy
plt.plot(history_1.history['accuracy'])
plt.plot(history_1.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss

plt.plot(history_1.history['loss'])
plt.plot(history_1.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

