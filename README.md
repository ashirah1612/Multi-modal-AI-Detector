<-----------MULTI-MODAL AI CONTENT DETECTOR--------->

A CNN-based web application designed to detect and analyze AI-generated content across multiple formats, including images and videos. The system helps identify whether digital content is real or AI-generated and also determines the source AI model used for image generation.

---

##  Features

- **AI Image Detection**
  - Classifies images as **Real** or **AI-generated**
  - Uses a custom-trained Convolutional Neural Network (CNN)

- **AI Model Detection**
  - Identifies the source model of AI-generated images
  - Supports models such as:
    - DALL·E  
    - MidJourney  
    - Stable Diffusion  
    - Flux  
  - Built using transfer learning (ResNet50)

-  **AI Video Detection**
  - Extracts frames using OpenCV
  - Performs frame-by-frame analysis using CNN
  - Calculates percentage of AI-generated content

---

## Tech Stack

- **Backend:** Flask (Python)  
- **Machine Learning:** TensorFlow, Keras  
- **Computer Vision:** OpenCV  
- **Frontend:** HTML, CSS, JavaScript  
- **Image Processing:** Pillow, NumPy  

---

##  Project Structure

multi-modal-ai-detector/
│
├── app.py  
├── requirements.txt  
├── README.md  
│
├── model.h5  
│
├── static/  
│   ├── css/  
│   ├── js/  
│   ├── images/  
│
├── templates/  
│   ├── home.html  
│   ├── modelch.html  
│   ├── vid.html  
│   ├── about.html  
│   ├── navbar.html  
│   └── footer.html  

---

## How to Run Locally

1. Clone the repository:
   git clone https://github.com/your-username/multi-modal-ai-detector.git

2. Navigate to the project folder:
   cd multi-modal-ai-detector

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python app.py

5. Open in browser:
   http://127.0.0.1:5000/


---

## 📸 Screenshots

- Home Page  
- AI Image Detection  
- AI Model Detection  
- AI Video Detection  

---

## ⚠️ Note

Due to GitHub file size limitations, large model files such as `model_module2.h5` are not included in the repository. The system is designed to load these models during runtime.

---

## 🌐 Deployment

The project can be deployed using platforms like:
- Render  
- Railway  

---

## 📌 Future Enhancements

- Improve model accuracy with larger datasets  
- Optimize video processing speed  
- Deploy full working system with hosted models  
- Add real-time detection API  

---

## 👩‍💻 Author

**Aseera Parveen J**  
CNN-Based Multi-Modal AI Detection System  

---

## 📜 License

This project is developed for academic purposes.
