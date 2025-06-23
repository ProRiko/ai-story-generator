# 🧠 AI Story & Video Generator

A web application that uses **Generative AI** to create engaging stories based on user prompts, with a conceptual backend foundation for future video generation. It showcases frontend-backend communication, secure API key handling, and integration of cutting-edge AI models like Google’s Gemini.

---

## 📚 Table of Contents

- [✨ Features](#-features)
- [🛠 Technologies Used](#-technologies-used)
- [📁 Project Structure](#-project-structure)
- [🚀 Setup Instructions](#-setup-instructions)
  - [🔧 Prerequisites](#-prerequisites)
  - [🔑 Obtaining API Keys](#-obtaining-api-keys)
  - [🧩 Backend Setup](#-backend-setup-python-flask)
  - [🎨 Frontend Setup](#-frontend-setup-htmlcssjs)
- [▶️ How to Run the Application](#️-how-to-run-the-application)
- [🎞 Conceptual Video Generation](#-conceptual-video-generation)
- [🔮 Future Enhancements](#-future-enhancements)
- [📄 License](#-license)

---

## ✨ Features

- **📝 AI-Powered Story Generator:** Generate short, medium, or long stories using Google Gemini API.
- **🔊 Text-to-Speech Integration:** Listen to your story using the browser’s native Web Speech API.
- **🎬 Conceptual Video Generation:** Backend lays the foundation for creating story-based videos (debug/demo only).
- **🔐 Secure API Handling:** All API keys are securely managed on the backend.
- **🌐 Full-Stack Architecture:** Smooth communication between frontend and backend over REST API.

---

## 🛠 Technologies Used

### Frontend:
- HTML5  
- CSS3 (Tailwind CSS for utility-first design)  
- JavaScript (ES6+)  
- Web Speech API (for TTS)

### Backend:
- Python 3  
- Flask (Web framework)  
- `requests` (for API calls)  
- `flask-cors` (CORS handling)

### AI Services:
- [Google Gemini API](https://aistudio.google.com/) (story generation)
- (Optional) [DeepAI API](https://deepai.org/) or Google Imagen (image generation)
- (Optional) Google Cloud Text-to-Speech (for real audio)

---

## 📁 Project Structure

ai_story_generator/

├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
└── backend/
└── backend.py

## 🚀 Setup Instructions

### 🔧 Prerequisites

- **Python 3.8+** (add to PATH during installation)
- **pip** (comes with Python)

---

### 🔑 Obtaining API Keys

#### Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Log in & create an API Key.
3. Copy the key securely for use in the backend.

#### (Optional) DeepAI API
1. Go to [DeepAI.org](https://deepai.org/)
2. Sign up & get your free API Key.

#### (Optional) Google Imagen API
- Requires Google Cloud billing enabled.
- Enable **Vertex AI API** in your Google Cloud project.

---

### 🧩 Backend Setup (Python Flask)

1. Navigate to the backend folder:

2. Install dependencies:
pip install Flask requests flask-cors

3. Set your API Key(s) as environment variables:

Windows (PowerShell):
$env:GEMINI_API_KEY="YOUR_GOOGLE_API_KEY"

4.Start the backend server:
python backend.py

🎨 Frontend Setup (HTML/CSS/JS)
Open a new terminal window.

1. Navigate to the frontend folder:

2. Serve the frontend using a simple HTTP server:
python -m http.server 8000

3. Open your browser and go to:
http://localhost:8000/index.html

🔮 Future Enhancements

🎥 Full Video Generation via FFmpeg and real TTS/Image tools.

🖼 Scene Matching Visuals per paragraph/scene.

🎵 Background Music Options and UI controls.

☁️ Database Support for storing user history.

📲 Social Media Integration (YouTube, Instagram).

👤 User Login & Saved Stories with personalization.


