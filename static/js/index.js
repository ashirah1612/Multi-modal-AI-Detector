
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
