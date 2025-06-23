# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import base64
import json
# import moviepy.editor as mp # Example: For basic video editing, might need ffmpeg
# from google.cloud import texttospeech # Example: For Google Cloud Text-to-Speech

app = Flask(__name__)
CORS(app) # Enable CORS for frontend-backend communication

# --- Configuration (replace with environment variables in production) ---
# IMPORTANT: In a real application, these API keys should NEVER be hardcoded
# and should be loaded securely from environment variables or a secret manager.
# You MUST set these as environment variables when running this backend.
# Example (in your terminal before running 'python backend.py'):
# export GEMINI_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY"
# export IMAGEN_API_KEY="YOUR_GOOGLE_CLOUD_IMAGEN_API_KEY" # Only if you enable billing for Imagen
# export DEEPAI_API_KEY="YOUR_DEEPAI_API_KEY" # Only if you choose DeepAI for images
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") 
IMAGEN_API_KEY = os.getenv("IMAGEN_API_KEY", "") 
DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY", "") 
# GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY", "") # Your actual Google Cloud TTS API Key

# --- AI Model Endpoints (these are called by the backend, not directly by frontend anymore) ---
GEMINI_FLASH_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
IMAGEN_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
DEEPAI_TEXT2IMG_API_URL = "https://api.deepai.org/api/text2img" # Free tier option

@app.route('/')
def health_check():
    """Simple health check endpoint."""
    return "Backend is running!"

@app.route('/generate_story', methods=['POST'])
def generate_story_backend():
    """
    Endpoint to generate a story using Gemini Flash.
    This proxies the call to Gemini API securely.
    """
    print("DEBUG: Entered generate_story_backend function.")
    data = request.json
    prompt = data.get('prompt')
    length = data.get('length', 'medium')

    print(f"DEBUG: Received prompt: '{prompt}', length: '{length}'")

    if not prompt:
        print("ERROR: Prompt is missing.")
        return jsonify({"error": "Prompt is required"}), 400
    
    print(f"DEBUG: GEMINI_API_KEY (from os.getenv): '{GEMINI_API_KEY}'")
    if not GEMINI_API_KEY:
        print("ERROR: Gemini API Key is not set on the backend server (environment variable is empty).")
        return jsonify({"error": "Gemini API Key is not set on the backend server."}), 500

    full_prompt = f"Generate a captivating story. Theme/Topic: \"{prompt}\". Length: {length}."
    if length == 'short':
        full_prompt += " Focus on a concise plot and impactful ending (1-2 paragraphs)."
    elif length == 'medium':
        full_prompt += " Develop a brief plot with a clear beginning, middle, and end (3-5 paragraphs)."
    elif length == 'long':
        full_prompt += " Create a more detailed narrative with character development, rising action, and a resolution (6+ paragraphs)."

    print(f"DEBUG: Full prompt prepared for Gemini: '{full_prompt}'")

    try:
        payload = {"contents": [{"role": "user", "parts": [{"text": full_prompt}]}]}
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY} 

        print(f"DEBUG: Sending request to Gemini API URL: {GEMINI_FLASH_API_URL} with payload: {json.dumps(payload)}")
        response = requests.post(GEMINI_FLASH_API_URL, headers=headers, params=params, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes

        result = response.json()
        print(f"DEBUG: Received response from Gemini API (partial): {str(result)[:200]}...") # Print first 200 chars
        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            story_text = result["candidates"][0]["content"]["parts"][0]["text"]
            print("DEBUG: Story extracted successfully.")
            return jsonify({"story": story_text}), 200
        else:
            print(f"ERROR: Failed to extract story from AI response. Full response: {result}")
            return jsonify({"error": "Failed to extract story from AI response"}), 500

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Error calling Gemini API: {e}")
        # If response.text exists and is not empty, include it for more details
        error_details = ""
        if hasattr(e, 'response') and e.response is not None and e.response.text:
            error_details = f" - Response content: {e.response.text}"
        return jsonify({"error": f"Failed to generate story due to API error: {e}{error_details}"}), 500
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route('/generate_visual', methods=['POST'])
def generate_visual_backend():
    """
    Endpoint to generate a visual. This now supports DeepAI for free tier.
    """
    print("DEBUG: Entered generate_visual_backend function.")
    data = request.json
    story_text = data.get('story_text')
    use_imagen = data.get('use_imagen', False) # Flag to choose Imagen vs DeepAI

    if not story_text:
        print("ERROR: Story text is missing for visual generation.")
        return jsonify({"error": "Story text is required"}), 400

    image_prompt = story_text # Default to full story text for prompt

    # Summarize story for image prompt using Gemini Flash (requires GEMINI_API_KEY)
    print(f"DEBUG: GEMINI_API_KEY for summarization: '{GEMINI_API_KEY}'")
    if GEMINI_API_KEY:
        try:
            summary_prompt = f"Summarize the essence of the following story in one highly visual sentence for an image generation AI:\n\n\"{story_text}\""
            print(f"DEBUG: Sending summary prompt to Gemini Flash: '{summary_prompt}'")
            summary_payload = {"contents": [{"role": "user", "parts": [{"text": summary_prompt}]}]}
            headers = {"Content-Type": "application/json"}
            params = {"key": GEMINI_API_KEY}

            summary_response = requests.post(GEMINI_FLASH_API_URL, headers=headers, params=params, json=summary_payload)
            summary_response.raise_for_status()
            summary_result = summary_response.json()

            if summary_result.get("candidates") and summary_result["candidates"][0].get("content") and summary_result["candidates"][0]["content"].get("parts"):
                image_prompt = summary_result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"DEBUG: Story summarized successfully for visual: '{image_prompt}'")
            else:
                print(f"WARNING: Failed to extract summary from Gemini response. Using full story text. Full response: {summary_result}")

        except requests.exceptions.RequestException as e:
            print(f"WARNING: Error calling Gemini API for summary, using full story text. Error: {e}")
            if hasattr(e, 'response') and e.response is not None and e.response.text:
                print(f"WARNING: Gemini summary response content: {e.response.text}")
        except Exception as e:
            print(f"WARNING: Unexpected error during summary, using full story text. Error: {e}")
    else:
        print("WARNING: GEMINI_API_KEY not set on backend, cannot summarize for visual. Using full story text.")


    # --- Image Generation Logic (Choose based on 'use_imagen' flag) ---
    if use_imagen:
        print(f"DEBUG: Attempting to generate visual with Imagen. IMAGEN_API_KEY: '{IMAGEN_API_KEY}'")
        if not IMAGEN_API_KEY:
            print("ERROR: Imagen API Key is not set on the backend server, or billing is not enabled for Imagen.")
            return jsonify({"error": "Imagen API Key is not set on the backend server, or billing is not enabled for Imagen."}), 500
        try:
            image_payload = {"instances": {"prompt": image_prompt}, "parameters": {"sampleCount": 1}}
            headers = {"Content-Type": "application/json"}
            params = {"key": IMAGEN_API_KEY}

            print(f"DEBUG: Sending request to Imagen API URL: {IMAGEN_API_URL} with payload: {json.dumps(image_payload)}")
            image_response = requests.post(IMAGEN_API_URL, headers=headers, params=params, json=image_payload)
            image_response.raise_for_status()

            image_result = image_response.json()
            if image_result.get("predictions") and image_result["predictions"][0].get("bytesBase64Encoded"):
                print("DEBUG: Imagen image extracted successfully.")
                image_data_base64 = image_result["predictions"][0]["bytesBase64Encoded"]
                return jsonify({"image_base64": image_data_base64, "image_prompt_used": image_prompt, "source": "Imagen"}), 200
            else:
                print(f"ERROR: Failed to extract image from Imagen AI response. Full response: {image_result}")
                return jsonify({"error": "Failed to extract image from Imagen AI response"}), 500
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Error calling Imagen API: {e}")
            error_details = ""
            if hasattr(e, 'response') and e.response is not None and e.response.text:
                error_details = f" - Response content: {e.response.text}"
            return jsonify({"error": f"Failed to generate image with Imagen due to API error: {e}{error_details}"}), 500
        except Exception as e:
            print(f"ERROR: An unexpected error occurred during Imagen generation: {e}")
            return jsonify({"error": f"An unexpected error occurred during Imagen generation: {e}"}), 500
    else: # Use DeepAI for free image generation
        print(f"DEBUG: Attempting to generate visual with DeepAI. DEEPAI_API_KEY: '{DEEPAAI_API_KEY}'")
        if not DEEPAI_API_KEY:
            print("ERROR: DeepAI API Key is not set on the backend server for free image generation.")
            return jsonify({"error": "DeepAI API Key is not set on the backend server for free image generation."}), 500
        try:
            deepai_payload = {'text': image_prompt}
            headers = {'api-key': DEEPAI_API_KEY}

            print(f"DEBUG: Sending request to DeepAI API URL: {DEEPAI_TEXT2IMG_API_URL} with payload: {deepai_payload}")
            image_response = requests.post(DEEPAI_TEXT2IMG_API_URL, data=deepai_payload, headers=headers)
            image_response.raise_for_status()

            result = image_response.json()
            if result.get("output_url"):
                print(f"DEBUG: DeepAI image URL received: {result['output_url']}")
                return jsonify({"image_url": result["output_url"], "image_prompt_used": image_prompt, "source": "DeepAI"}), 200
            else:
                print(f"ERROR: Failed to extract image URL from DeepAI response. Full response: {result}")
                return jsonify({"error": "Failed to extract image URL from DeepAI response"}), 500
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Error calling DeepAI API: {e}")
            error_details = ""
            if hasattr(e, 'response') and e.response is not None and e.response.text:
                error_details = f" - Response content: {e.response.text}"
            return jsonify({"error": f"Failed to generate image with DeepAI due to API error: {e}{error_details}"}), 500
        except Exception as e:
            print(f"ERROR: An unexpected error occurred during DeepAI generation: {e}")
            return jsonify({"error": f"An unexpected error occurred during DeepAI generation: {e}"}), 500


@app.route('/generate_video', methods=['POST'])
def generate_video():
    """
    CONCEPTUAL ENDPOINT: This function outlines the steps a backend would take
    to generate a video from a story. Actual implementation requires external
    libraries and services (like FFmpeg, TTS clients).
    """
    print("DEBUG: Entered generate_video function.")
    data = request.json
    story_text = data.get('story_text')
    image_prompt = data.get('image_prompt', story_text) # Fallback to story_text if not provided

    if not story_text:
        print("ERROR: Story text is missing for video generation.")
        return jsonify({"error": "Story text is required"}), 400
    
    print(f"DEBUG: GEMINI_API_KEY for video process: '{GEMINI_API_KEY}'")
    if not GEMINI_API_KEY:
        print("ERROR: Gemini API Key is required on backend for video process (cannot summarize for image/voice).")
        return jsonify({"error": "Gemini API Key is required on backend for video process."}), 500
    
    # Decide which image API to use (DeepAI as default for free tier conceptual video)
    # If IMAGEN_API_KEY is set and billing enabled, you might prioritize it.
    print(f"DEBUG: DEEPAI_API_KEY for video visual: '{DEEPAI_API_KEY}'")
    print(f"DEBUG: IMAGEN_API_KEY for video visual: '{IMAGEN_API_KEY}'")
    if not (IMAGEN_API_KEY or DEEPAI_API_KEY):
        print("ERROR: An image API Key (Imagen or DeepAI) is required for video process.")
        return jsonify({"error": "An image API Key (Imagen or DeepAI) is required for video process."}), 500


    print(f"DEBUG: Attempting to generate conceptual video for story: {story_text[:50]}...")

    try:
        # Step 1: Generate Audio from Text (Conceptual)
        # This would typically involve calling a Text-to-Speech (TTS) API (e.g., Google Cloud Text-to-Speech).
        # Requires: google-cloud-texttospeech library and a specific API key if not part of general Gemini key
        # Example:
        # from google.cloud import texttospeech
        # client = texttospeech.TextToSpeechClient()
        # synthesis_input = texttospeech.SynthesisInput(text=story_text)
        # voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        # audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        # response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        # with open("story_audio.mp3", "wb") as out:
        #     out.write(response.audio_content)
        # audio_file_path = "story_audio.mp3"
        
        # Placeholder for demonstration:
        audio_file_path = "conceptual_audio.mp3" 
        print(f"Conceptual: Audio generated and saved to {audio_file_path}")


        # Step 2: Generate or retrieve Visuals (Conceptual)
        # This could involve calling either Imagen or DeepAI (based on your preference/billing)
        # or generating multiple images for a sequence.
        # For simplicity, we'll imagine generating ONE image for the video.
        print("DEBUG: Calling generate_visual_backend for video visual...")
        # Assuming DeepAI as default for video visual for free tier compatibility
        visual_data_response = requests.post(request.url_root + 'generate_visual', json={"story_text": story_text, "use_imagen": False})
        visual_data_response.raise_for_status() # Raise error for bad status
        visual_data = visual_data_response.json()

        if "error" in visual_data:
            raise Exception(f"Failed to get visual for video: {visual_data['error']}")
        
        visual_url = visual_data.get("image_url") # Expecting URL from DeepAI
        visual_base64 = visual_data.get("image_base64") # Expecting base64 from Imagen

        visual_file_path = "conceptual_visual.png" # Default placeholder path
        if visual_url:
             print(f"DEBUG: Visual URL for video: {visual_url}")
             # Download image from URL and save to file
             image_response = requests.get(visual_url)
             if image_response.ok:
                 with open(visual_file_path, "wb") as f:
                     f.write(image_response.content)
                 print(f"Conceptual: Visual downloaded and saved to {visual_file_path}")
             else:
                 raise Exception(f"Failed to download visual from URL: {visual_url}")
        elif visual_base64:
             print("DEBUG: Visual base64 data for video detected (from Imagen).")
             try:
                 with open(visual_file_path, "wb") as fh:
                     fh.write(base64.b64decode(visual_base64))
                 print(f"Conceptual: Imagen visual saved to {visual_file_path}")
             except Exception as img_save_err:
                 raise Exception(f"Failed to save base64 image for video: {img_save_err}")
        else:
             print("WARNING: No visual data (URL or base64) received for video. Using placeholder.")


        # Step 3: Combine Audio and Visuals into Video (Conceptual)
        # Requires: FFmpeg installed on the server, and potentially moviepy Python library.
        # Duration of the video should match the audio length for simple cases.
        # Example using moviepy (which relies on ffmpeg):
        # clip = mp.ImageClip(visual_file_path).set_duration(mp.AudioFileClip(audio_file_path).duration)
        # audioclip = mp.AudioFileClip(audio_file_path)
        # final_clip = clip.set_audio(audioclip)
        # output_video_path = "output_story_video.mp4"
        # final_clip.write_videofile(output_video_path, fps=24, codec="libx264")

        # Placeholder for demonstration:
        output_video_path = "output_story_video.mp4"
        print(f"Conceptual: Video created and saved to {output_video_path}")

        # Step 4: Upload to Cloud Storage and Get URL (Conceptual)
        # This would involve using cloud storage SDKs (e.g., google.cloud.storage, boto3)
        # For a full implementation, you'd upload output_video_path to Google Cloud Storage or similar.
        cloud_video_url = "https://example.com/conceptual_video_link.mp4" # Placeholder
        print(f"Conceptual: Video uploaded to cloud storage: {cloud_video_url}")

        # Step 5: (Optional) Post to Social Media (Conceptual)
        # This would involve using specific social media APIs (e.g., Facebook Graph API, YouTube Data API)
        # and would require OAuth authentication and adherence to platform policies.
        # Example: post_to_facebook(cloud_video_url, "My new AI story video!")
        print("Conceptual: Social media posting would occur here.")

        return jsonify({"message": "Video generation process initiated conceptually. Video URL is placeholder.", "video_url": cloud_video_url}), 200

    except Exception as e:
        print(f"ERROR: Error during conceptual video generation: {e}")
        return jsonify({"error": f"Failed to generate video: {e}"}), 500

if __name__ == '__main__':
    # When running locally, ensure you set API keys as environment variables
    # before running this script.
    # To run: python backend.py
    # This will run on http://127.0.0.1:5000/
    app.run(debug=True, port=5000)
