import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
import os

# dataset paths
train_dir = "dataset/train"
test_dir = "dataset/test"

# image settings
img_size = (128, 128)
batch_size = 8

# load dataset
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=img_size,
    batch_size=batch_size
)

#  GET CLASS NAMES BEFORE MAP
class_names = train_data.class_names
print("Classes:", class_names)

test_data = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=img_size,
    batch_size=batch_size
)

# normalize
train_data = train_data.map(lambda x, y: (x / 255.0, y))
test_data = test_data.map(lambda x, y: (x / 255.0, y))

# model
model = models.Sequential([
    layers.Conv2D(16, (3,3), activation='relu', input_shape=(128,128,3)),
    layers.MaxPooling2D(),

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(2, activation='softmax')   # 2 classes: ai, real
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# train
model.fit(
    train_data,
    validation_data=test_data,
    epochs=5
)

# save model
model.save("model.h5")

print("Model trained and saved!")