import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras import layers, models  # type: ignore
from tqdm import tqdm

# ================= CONFIG =================
DATASET_PATH = "dataset3"
IMG_HEIGHT = 128
IMG_WIDTH = 128
DURATION = 8  # seconds
SAMPLE_RATE = 22050

# ================= AUDIO → MEL =================
def preprocess_audio(file_path):
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    target_length = sr * DURATION

    if len(y) > target_length:
        y = y[:target_length]
    else:
        y = np.pad(y, (0, target_length - len(y)))

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=128,
        hop_length=512
    )

    mel_db = librosa.power_to_db(mel, ref=np.max)

    # normalize
    denominator = (mel_db.max() - mel_db.min())
    if denominator != 0:
        mel_db = (mel_db - mel_db.min()) / denominator
    else:
        mel_db = np.zeros_like(mel_db)

    # resize to fixed shape
    mel_db = tf.image.resize(mel_db[..., np.newaxis], (IMG_HEIGHT, IMG_WIDTH))

    return mel_db.numpy()


# ================= LOAD DATA =================
def load_data(folder):
    X = []
    y = []

    classes = ["ai", "real"]

    for label, cls in enumerate(classes):
        path = os.path.join(folder, cls)

        for file in tqdm(os.listdir(path), desc=f"Loading {cls}"):
            file_path = os.path.join(path, file)

            try:
                mel = preprocess_audio(file_path)
                X.append(mel)
                y.append(label)
            except:
                continue

    return np.array(X), np.array(y)


print("Loading training data...")
X_train, y_train = load_data(os.path.join(DATASET_PATH, "train"))

print("Loading validation data...")
X_val, y_val = load_data(os.path.join(DATASET_PATH, "val"))

# ================= BUILD MODEL =================
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 1)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),

    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),

    layers.Dense(2, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ================= TRAIN =================
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=15,
    batch_size=32
)
print("Final Training Accuracy:", history.history['accuracy'][-1])
print("Final Validation Accuracy:", history.history['val_accuracy'][-1])

# ================= SAVE MODEL =================
model.save("model_audio.h5")

print("Model saved as model_audio.h5")