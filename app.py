from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image  # type: ignore
from PIL import Image
import time
import cv2
import uuid
import os
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key_here'

# ===== UPLOAD FOLDER =====
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ===== LOAD MODELS =====
model1 = tf.keras.models.load_model("model.h5")             
model2 = tf.keras.models.load_model("model_module2.h5")     

# ===== CLASS NAMES =====
class_names_1 = ['ai', 'real']
class_names_2 = ['dalle', 'flux', 'midjourney', 'stabdiff']

# ===== VIDEO CONFIG =====
MAX_VIDEO_SECONDS = 15
FRAME_RATE = 1
IMG_SIZE_VIDEO = (128, 128)
AI_NOISE_THRESHOLD = 2.0

#  MODULE 1 


@app.route('/')
def home():
    return render_template(
        'index.html',
        result=session.pop('result', None),
        confidence=session.pop('confidence', None),
        image_file=session.pop('image_file', None)
    )


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('image')

    if not file:
        return redirect(url_for('home'))

    # clear uploads
    for f in os.listdir(UPLOAD_FOLDER):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        except:
            pass

    filename = str(int(time.time())) + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model1.predict(img_array)
    predicted_class = class_names_1[np.argmax(prediction)]
    confidence = float(np.max(prediction)) * 100

    session['result'] = predicted_class.upper()
    session['confidence'] = round(confidence, 2)
    session['image_file'] = filename

    return redirect(url_for('home'))


#  MODULE 2 
@app.route('/model2', methods=['GET', 'POST'])
def model2_page():
    result = None
    confidence = None
    image_file = None

    if request.method == 'POST':
        file = request.files.get('image')

        if file:
            filename = str(int(time.time())) + ".jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_file = filename

            # DIRECTLY detect AI model (NO AI/REAL CHECK)
            img = Image.open(filepath).convert("RGB")
            img = img.resize((224, 224))
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            pred = model2.predict(img)[0]
            idx = np.argmax(pred)

            result = class_names_2[idx]
            confidence = round(pred[idx] * 100, 2)

    return render_template(
        "modelch.html",
        result=result,
        confidence=confidence,
        image_file=image_file
    )

#  MODULE 3

@app.route('/video')
def video_page():
    return render_template('vid.html')

def preprocess_frame(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (128, 128))   
    img = resized / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total / fps

    duration = min(duration, MAX_VIDEO_SECONDS)

    frames = []
    for sec in range(int(duration)):
        frame_id = int(sec * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames


def analyse_video_frames(frames):
    total = len(frames)
    ai_count = 0

    for frame in frames:
        inp = preprocess_frame(frame)
        pred = model1.predict(inp)[0]

        if pred.shape[0] == 1:
            is_ai = pred[0] > 0.5
        else:
            is_ai = np.argmax(pred) == 0

        if is_ai:
            ai_count += 1

    ai_pct = (ai_count / total) * 100 if total > 0 else 0

    if ai_pct <= AI_NOISE_THRESHOLD:
        ai_pct = 0

    return total, ai_count, round(ai_pct, 1)


@app.route('/analyse-video', methods=['POST'])
def analyse_video():
    file = request.files.get('video')

    if not file:
        return jsonify({"error": "No video uploaded"})

    filename = str(uuid.uuid4()) + ".mp4"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    frames = extract_frames(path)

    if not frames or len(frames) == 0:
         return jsonify({"error": "No frames extracted from video"})

    print("Frames extracted:", len(frames))

    total, ai_frames, ai_pct = analyse_video_frames(frames)

    os.remove(path)

    return jsonify({
        "total_frames": total,
        "ai_frames": ai_frames,
        "ai_percentage": ai_pct,
        "detected": ai_pct > 0,
        "verdict": (
            f"AI Content Detected: {ai_pct}%"
            if ai_pct > 0
            else "No significant AI content detected (0%)"
        )
    })




@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/vid')
def vid():
    return render_template('vid.html')


if __name__ == '__main__':
    app.run(debug=True)
