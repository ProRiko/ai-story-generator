AI Story & Video Generator
A web application that leverages generative AI to create engaging stories and conceptually lays the groundwork for generating accompanying videos. This project demonstrates frontend-backend communication, secure API key handling, and the integration of large language models.

Table of Contents
Features

Technologies Used

Project Structure

Setup Instructions

Prerequisites

Obtaining API Keys

Backend Setup (Python Flask)

Frontend Setup (HTML/CSS/JS)

How to Run the Application

Understanding Conceptual Video Generation

Future Enhancements

License

Features
AI Story Generation: Generate captivating stories of various lengths (short, medium, long) based on user prompts, powered by Google's Gemini API.

Text-to-Speech: Listen to the generated stories read aloud using the browser's native Web Speech API.

Conceptual Video Generation: The backend provides a conceptual endpoint for video creation, outlining the steps required to combine story audio and visuals into a video file (requires further implementation and external tools).

Secure API Key Handling: API keys for AI services are handled securely on the backend, preventing their exposure in client-side code.

Technologies Used
Frontend:

HTML5

CSS3 (with Tailwind CSS for utility-first styling)

JavaScript (ES6+)

Web Speech API (for text-to-speech)

Backend:

Python 3

Flask (Web framework)

requests library (for making HTTP requests to external APIs)

flask-cors (for handling Cross-Origin Resource Sharing)

AI Services (accessed via backend):

Google Gemini API (for story generation and summarization)

(Optional, for full video implementation: Google Imagen API or DeepAI API for image generation, Google Cloud Text-to-Speech for audio)

Project Structure
my_ai_content_creator/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── backend/
    └── backend.py

Setup Instructions
Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.8+: Download from python.org. Make sure to select "Add Python to PATH" during installation.

pip: Python's package installer (usually comes with Python).

Obtaining API Keys
This project relies on AI services, which require API keys. Your keys will be used by the backend server and should never be hardcoded directly into your frontend files when deployed.

Google AI Studio API Key (for Gemini):

Go to Google AI Studio.

Log in with your Google account.

Create a new API key or copy an existing one. This key grants access to the Gemini model.

(Optional) DeepAI API Key (for free image generation, if you re-enable it in backend.py):

Go to DeepAI.

Sign up for a free account.

Navigate to your dashboard to find and copy your API Key. No credit card is required for their free tier.

(Optional) Google Imagen API Key (for image generation, requires Google Cloud billing enabled):

If you wish to use Google's Imagen for higher-quality image generation, you will need to enable billing for a Google Cloud Project and ensure the Vertex AI API is enabled. You can manage this in the Google Cloud Console.

Backend Setup (Python Flask)
Navigate to the backend directory:
Open your terminal or command prompt and change to the backend directory of your project:

cd my_ai_content_creator/backend

Install Python dependencies:

pip install Flask requests flask-cors

Set your API Keys as Environment Variables:
This is crucial for security. Your backend.py script reads these keys from your environment.

Replace YOUR_GOOGLE_AI_STUDIO_API_KEY with the actual key you obtained.

If using DeepAI/Imagen for visuals through the backend, uncomment and set those too.

On macOS / Linux:

export GEMINI_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY"
# export DEEPAI_API_KEY="YOUR_DEEPAI_API_KEY"
# export IMAGEN_API_KEY="YOUR_GOOGLE_CLOUD_IMAGEN_API_KEY"

On Windows (Command Prompt):

set GEMINI_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY"
REM set DEEPAI_API_KEY="YOUR_DEEPAI_API_KEY"
REM set IMAGEN_API_KEY="YOUR_GOOGLE_CLOUD_IMAGEN_API_KEY"

On Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY"
# $env:DEEPAAI_API_KEY="YOUR_DEEPAI_API_KEY"
# $env:IMAGEN_API_KEY="YOUR_GOOGLE_CLOUD_IMAGEN_API_KEY"

Start the Flask backend server:

python backend.py

Keep this terminal window open. The server must be running for the frontend to function. You should see output indicating it's running on http://127.0.0.1:5000/.

Frontend Setup (HTML/CSS/JS)
The frontend files (index.html, style.css, script.js) are ready to be served. No direct API keys are hardcoded in script.js; it communicates with your backend.

How to Run the Application
Once your backend server is running (Step 3 above):

Open a new terminal or command prompt window.

Navigate to the frontend directory:

cd my_ai_content_creator/frontend

Start a simple Python HTTP server to serve the frontend files:

python -m http.server 8000

(You can use any available port, e.g., python -m http.server 5500. Remember the port number.)

Open your web browser and navigate to:

http://localhost:8000/index.html

(Replace 8000 with your chosen port if different.)

You should now see the "AI Story & Video Generator" web application. Enter a prompt and click "Generate Story."

Understanding Conceptual Video Generation
The "Generate Video" feature in this project is currently conceptual. This means:

The frontend sends a request to your backend.

Your backend.py prints debug messages outlining the steps it would take (e.g., "Conceptual: Audio generated...", "Conceptual: Visual generated...", "Conceptual: Video created and saved...").

It returns a placeholder URL (https://example.com/conceptual_video_link.mp4).

Actual video generation (combining audio and multiple images into a playable MP4 file) is a complex task that typically requires:

FFmpeg: A powerful external command-line tool for multimedia processing, installed on your backend server.

Cloud Text-to-Speech API: To generate audio files from the story text (often incurs costs).

Image Generation/Retrieval: Generating or fetching multiple images relevant to the story's scenes.

Cloud Storage: For storing the generated video files, as they can be large.

Future Enhancements
Full Video Generation: Implement FFmpeg and actual TTS/Image generation services in the backend to create real video files.

Multiple Scene Visuals: Generate or select several images to match different parts of the story for a more dynamic video.

Social Media Posting: Integrate with social media APIs (e.g., YouTube Data API, Facebook Graph API) to allow direct posting of generated videos.

User Interface for Video Options: Add controls for video style, background music, or different voice options.

Database Integration: Store generated stories and video links in a database for user history.

License
This project is open-source and available under the MIT License.
