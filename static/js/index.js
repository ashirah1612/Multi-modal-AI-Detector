
document.addEventListener("DOMContentLoaded", () => {
    const preview = document.getElementById("previewImage");

    if (preview) preview.style.display = "none";
});


// IMAGE DETECTOR PAGE 

const uploadArea = document.querySelector('.upload-area');

const uploadInput = document.getElementById('fileInput');

const resultCard = document.querySelector('.result-card');
const detectButton = document.querySelector('#detectButton');

if (uploadArea && uploadInput && detectButton) {

    uploadArea.addEventListener('click', () => uploadInput.click());

    uploadInput.addEventListener('change', (e) => {
        const file = e.target.files[0];

        if (file) {
            document.getElementById("fileName").innerText = file.name + " ✅ Uploaded";
            document.getElementById("uploadText").style.display = "none";

            const reader = new FileReader();

            reader.onload = (e) => {
                const preview = document.getElementById("previewImage");
                preview.src = e.target.result;
                preview.style.display = "block";
            };

            reader.readAsDataURL(file);
        }
    });
}


// FAQ

document.querySelectorAll(".faq-question").forEach(item => {
    item.addEventListener("click", () => {

        const parent = item.parentElement;

        document.querySelectorAll(".faq-item").forEach(faq => {
            if (faq !== parent) {
                faq.classList.remove("active");
            }
        });

        parent.classList.toggle("active");
    });
});

//module 3

// ===== VIDEO MODULE =====

const videoInput = document.getElementById("videoInput");
const fileNameDisplay = document.getElementById("fileName");

if (videoInput) {
    videoInput.addEventListener("change", () => {
        fileNameDisplay.innerText = videoInput.files[0]?.name || "";
    });
}

function uploadVideo() {
    const file = videoInput.files[0];

    if (!file) {
        alert("Please upload a video");
        return;
    }

    const formData = new FormData();
    formData.append("video", file);

    fetch("/analyse-video", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("resultBox").style.display = "block";

        if (data.error) {
            document.getElementById("verdict").innerText = data.error;
            return;
        }

        document.getElementById("verdict").innerText = data.verdict;
        document.getElementById("details").innerText =
            `Frames: ${data.total_frames} | AI Frames: ${data.ai_frames} | AI %: ${data.ai_percentage}`;
    })
    .catch(err => {
        alert("Error processing video");
        console.error(err);
    });
}


function toggleMenu() {
    document.getElementById("navLinks").classList.toggle("active");
}



//audio

function uploadAudio() {
    const input = document.getElementById("audioInput");
    const file = input.files[0];

    if (!file) {
        alert("Please select an audio file");
        return;
    }

    const formData = new FormData();
    formData.append("audio", file);

    document.getElementById("loadingText").style.display = "block";
    document.getElementById("resultBox").style.display = "none";
    document.getElementById("errorText").innerText = "";
    document.getElementById("pulseLoader").style.display = "block";

    let dots = 0;
    const interval = setInterval(() => {
        dots = (dots + 1) % 4;
        document.getElementById("loadingText").innerText =
            "Analyzing" + ".".repeat(dots);
    }, 500);

    fetch("/predict-audio", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(interval);
        document.getElementById("pulseLoader").style.display = "none";
        document.getElementById("loadingText").style.display = "none";

        if (data.error) {
            document.getElementById("errorText").innerText = data.error;
            return;
        }

        const box = document.getElementById("resultBox");
        box.style.display = "block";
        box.style.opacity = 0;
        box.style.transform = "translateY(20px)";

        setTimeout(() => {
            box.style.transition = "all 0.4s ease";
            box.style.opacity = 1;
            box.style.transform = "translateY(0)";
        }, 50);

        const verdict = data.prediction;
        const confidence = data.confidence;

        document.getElementById("verdict").innerText =
            confidence + "% " + verdict.toUpperCase();

        document.getElementById("details").innerText = "Model Confidence";

        if (verdict.toLowerCase() === "real") {
            document.getElementById("topResult").innerHTML =
                "🧑 Real Audio (" + confidence + "%)";
        } else {
            document.getElementById("topResult").innerHTML =
                "🤖 AI Generated (" + confidence + "%)";
                      }
    })
    .catch(err => {
        clearInterval(interval);
        document.getElementById("pulseLoader").style.display = "none";
        document.getElementById("loadingText").style.display = "none";
        document.getElementById("errorText").innerText = "Something went wrong.";
    });
}


// file name display
const audioInput = document.getElementById("audioInput");

if (audioInput) {
    audioInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            document.getElementById("fileName").innerText = file.name;
            document.getElementById("resultBox").style.display = "none";
            document.getElementById("errorText").innerText = "";
        }
    });
}
