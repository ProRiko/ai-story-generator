const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

const storyPromptInput = document.getElementById('storyPrompt');
const storyLengthSelect = document.getElementById('storyLength');
const generateStoryBtn = document.getElementById('generateStoryBtn');
const generatedStoryTextarea = document.getElementById('generatedStory');
const loadingIndicator = document.getElementById('loadingIndicator');
const messageBox = document.getElementById('messageBox');
const messageText = document.getElementById('messageText');

// Function to show a custom message (instead of alert)
function showMessage(message, type = 'error') {
    messageText.textContent = message;
    messageBox.className = `px-4 py-3 rounded-md relative ${type === 'error' ? 'bg-red-100 border border-red-400 text-red-700' : 'bg-green-100 border border-green-400 text-green-700'}`;
    messageBox.classList.remove('hidden');
    setTimeout(() => {
        messageBox.classList.add('hidden');
    }, 5000); // Hide after 5 seconds
}

generateStoryBtn.addEventListener('click', async () => {
    const prompt = storyPromptInput.value.trim();
    const length = storyLengthSelect.value;

    if (!prompt) {
        showMessage('Please enter a story prompt or theme!', 'error');
        return;
    }

    generatedStoryTextarea.value = ''; // Clear previous story
    loadingIndicator.style.display = 'block'; // Show loading indicator
    generateStoryBtn.disabled = true; // Disable button during generation
    messageBox.classList.add('hidden'); // Hide any previous messages

    try {
        // Construct the prompt for the AI based on user input
        let fullPrompt = `Generate a captivating story.
        Theme/Topic: "${prompt}".
        Length: ${length}.`;

        if (length === 'short') {
            fullPrompt += ` Focus on a concise plot and impactful ending (1-2 paragraphs).`;
        } else if (length === 'medium') {
            fullPrompt += ` Develop a brief plot with a clear beginning, middle, and end (3-5 paragraphs).`;
        } else if (length === 'long') {
            fullPrompt += ` Create a more detailed narrative with character development, rising action, and a resolution (6+ paragraphs).`;
        }

        console.log("Sending prompt to AI:", fullPrompt);

        let chatHistory = [];
        chatHistory.push({ role: "user", parts: [{ text: fullPrompt }] });

        const payload = { contents: chatHistory };
        const apiKey = ""; // Canvas will automatically provide this key at runtime
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(`Failed to generate story: ${errorData.error ? errorData.error.message : response.statusText}`);
        }

        const result = await response.json();
        console.log("AI Response:", result);

        if (result.candidates && result.candidates.length > 0 &&
            result.candidates[0].content && result.candidates[0].content.parts &&
            result.candidates[0].content.parts.length > 0) {
            const text = result.candidates[0].content.parts[0].text;
            generatedStoryTextarea.value = text;
        } else {
            showMessage('Could not generate a story. The AI response was empty or malformed.', 'error');
        }

    } catch (error) {
        console.error("Error generating story:", error);
        showMessage(`Error generating story: ${error.message}`, 'error');
    } finally {
        loadingIndicator.style.display = 'none'; // Hide loading indicator
        generateStoryBtn.disabled = false; // Re-enable button
    }
});
