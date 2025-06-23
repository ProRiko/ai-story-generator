// Global variables for Firebase configuration (provided by the Canvas environment)
// These are not used for story generation with the Gemini API directly, but are good practice
// to include if you might expand to use Firestore later.
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

// --- DOM Elements ---
const storyPromptInput = document.getElementById('storyPrompt');
const storyLengthSelect = document.getElementById('storyLength');
const generateStoryBtn = document.getElementById('generateStoryBtn');
const generatedStoryTextarea = document.getElementById('generatedStory');
const readStoryBtn = document.getElementById('readStoryBtn');
const stopReadingBtn = document.getElementById('stopReadingBtn');
const generateVideoBtn = document.getElementById('generateVideoBtn'); // New button
const loadingIndicatorStory = document.getElementById('loadingIndicatorStory');
const loadingIndicatorVideo = document.getElementById('loadingIndicatorVideo'); // New loading indicator
const videoOutputDiv = document.getElementById('videoOutput'); // New div for video link
const videoLink = document.getElementById('videoLink'); // New link element
const messageBox = document.getElementById('messageBox');
const messageText = document.getElementById('messageText');

// --- Backend API Base URL ---
// When running locally, the Flask backend will typically be at this address.
// If you deploy your backend, this URL will change.
const BACKEND_URL = "http://127.0.0.1:5000";


// --- Web Speech API (for reading story aloud) ---
const synth = window.speechSynthesis;
let currentUtterance = null; // To keep track of the current speech utterance

// --- Utility Functions ---

/**
 * Displays a message box with a given message and type (error/success).
 * @param {string} message The message to display.
 * @param {'error'|'success'} type The type of message (determines styling).
 */
function showMessage(message, type = 'error') {
    messageText.textContent = message;
    messageBox.className = `px-4 py-3 rounded-md relative ${type === 'error' ? 'bg-red-100 border border-red-400 text-red-700' : 'bg-green-100 border border-green-400 text-green-700'}`;
    messageBox.classList.remove('hidden');
    setTimeout(() => {
        messageBox.classList.add('hidden');
    }, 5000); // Hide after 5 seconds
}

/**
 * Toggles the disabled state of buttons related to story/video actions.
 * @param {boolean} isDisabled Whether the buttons should be disabled.
 */
function toggleActionButtons(isDisabled) {
    readStoryBtn.disabled = isDisabled;
    generateVideoBtn.disabled = isDisabled;
    // stopReadingBtn disabled state is managed by speech events
}

// --- Event Listeners ---

// Generate Story Button Click (Calls Backend)
generateStoryBtn.addEventListener('click', async () => {
    const prompt = storyPromptInput.value.trim();
    const length = storyLengthSelect.value;

    if (!prompt) {
        showMessage('Please enter a story prompt or theme!', 'error');
        return;
    }

    // Clear previous outputs and disable buttons
    generatedStoryTextarea.value = '';
    videoOutputDiv.classList.add('hidden'); // Hide previous video link
    videoLink.href = '#';
    videoLink.textContent = '';
    
    loadingIndicatorStory.classList.remove('hidden');
    loadingIndicatorVideo.classList.add('hidden'); // Ensure video loading is hidden
    
    generateStoryBtn.disabled = true;
    toggleActionButtons(true); // Disable read and video buttons
    messageBox.classList.add('hidden');

    try {
        console.log("Sending story generation request to backend...");

        const response = await fetch(`${BACKEND_URL}/generate_story`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, length })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Backend Error (Story Generation):', errorData);
            throw new Error(`Failed to generate story: ${errorData.error || response.statusText}`);
        }

        const result = await response.json();
        console.log("Backend Story Response:", result);

        if (result.story) {
            generatedStoryTextarea.value = result.story;
            toggleActionButtons(false); // Enable read and video buttons
            showMessage('Story generated successfully!', 'success');
        } else {
            showMessage('Could not generate a story. Backend response was empty or malformed.', 'error');
        }

    } catch (error) {
        console.error("Error generating story:", error);
        showMessage(`Error generating story: ${error.message}. Ensure backend is running.`, 'error');
    } finally {
        loadingIndicatorStory.classList.add('hidden');
        generateStoryBtn.disabled = false;
    }
});

// Read Story Aloud Button Click
readStoryBtn.addEventListener('click', () => {
    const textToRead = generatedStoryTextarea.value.trim();
    if (!textToRead) {
        showMessage('No story to read!', 'error');
        return;
    }

    if (synth.speaking && currentUtterance) {
        synth.cancel(); // Stop any ongoing speech
    }

    currentUtterance = new SpeechSynthesisUtterance(textToRead);

    currentUtterance.onstart = () => {
        readStoryBtn.disabled = true;
        stopReadingBtn.disabled = false;
    };
    currentUtterance.onend = () => {
        readStoryBtn.disabled = false;
        stopReadingBtn.disabled = true;
    };
    currentUtterance.onerror = (event) => {
        console.error('Speech synthesis error:', event.error);
        showMessage(`Speech error: ${event.error}`, 'error');
        readStoryBtn.disabled = false;
        stopReadingBtn.disabled = true;
    };

    synth.speak(currentUtterance);
});

// Stop Reading Button Click
stopReadingBtn.addEventListener('click', () => {
    if (synth.speaking) {
        synth.cancel();
        readStoryBtn.disabled = false;
        stopReadingBtn.disabled = true;
    }
});

// Generate Video Button Click (Calls Backend)
generateVideoBtn.addEventListener('click', async () => {
    const storyText = generatedStoryTextarea.value.trim();
    if (!storyText) {
        showMessage('Generate a story first before generating a video!', 'error');
        return;
    }

    videoOutputDiv.classList.add('hidden'); // Hide previous video link
    videoLink.href = '#';
    videoLink.textContent = '';

    loadingIndicatorVideo.classList.remove('hidden');
    generateVideoBtn.disabled = true;
    readStoryBtn.disabled = true; // Disable read button during video generation
    stopReadingBtn.disabled = true; // Disable stop button
    messageBox.classList.add('hidden');

    try {
        console.log("Sending video generation request to backend...");
        
        const response = await fetch(`${BACKEND_URL}/generate_video`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ story_text: storyText })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Backend Error (Video Generation):', errorData);
            throw new Error(`Failed to generate video: ${errorData.error || response.statusText}`);
        }

        const result = await response.json();
        console.log("Backend Video Response:", result);

        if (result.video_url) {
            videoLink.href = result.video_url;
            videoLink.textContent = result.video_url;
            videoOutputDiv.classList.remove('hidden'); // Show video link
            showMessage('Video generation process initiated! See conceptual URL below.', 'success');
        } else {
            showMessage('Could not initiate video generation. Backend response was empty or malformed.', 'error');
        }

    } catch (error) {
        console.error("Error generating video:", error);
        showMessage(`Error generating video: ${error.message}. Ensure backend is running.`, 'error');
    } finally {
        loadingIndicatorVideo.classList.add('hidden');
        generateVideoBtn.disabled = false;
        readStoryBtn.disabled = false; // Re-enable read button
        if (!synth.speaking) { // Only re-enable stop if not currently speaking
             stopReadingBtn.disabled = true;
        }
    }
});
