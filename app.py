"""
Project: AI YouTube Fact Checker & Summarizer
Author: [Your Name]
Description: This Flask server acts as the backend. It takes a YouTube URL from the extension, 
             fetches the transcript (subtitles), and sends it to Google Gemini AI to generate a summary.
"""

import sys
import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai  # Google's latest AI library
from youtube_transcript_api import YouTubeTranscriptApi # To fetch captions/subtitles

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # This allows our Chrome Extension to talk to this Python Server (Cross-Origin Resource Sharing)

# --- CONFIGURATION ---
# TODO: Replace with your actual API Key. 
# For GitHub security, it's better to use Environment Variables (os.getenv), but for now, we paste it here.
GENAI_API_KEY = "AIzaSyANwcV2BbGfyYDJ1HHFs0DFo6k5nI8tU_Y" 

# Initialize Google AI Client
client = genai.Client(api_key=GENAI_API_KEY)

# --- HELPER FUNCTION: EXTRACT VIDEO ID ---
def get_youtube_id(url):
    """
    Parses a YouTube URL to extract the unique Video ID.
    Example: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' -> 'dQw4w9WgXcQ'
    """
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    return None

# --- MAIN API ROUTE ---
@app.route('/analyze', methods=['POST'])
def analyze():
    print("\n--- NEW REQUEST RECEIVED ---")
    
    # 1. Get URL from the Chrome Extension
    data = request.json
    url = data.get('url', '')
    video_id = get_youtube_id(url)

    if not video_id:
        return jsonify({"analysis": "Error: Invalid YouTube Link provided."})

    transcript_text = ""

    # 2. FETCH TRANSCRIPT (SUBTITLES)
    try:
        print(f"Fetching Transcript for Video ID: {video_id}")
        
        # Method A: Try to find Hindi or English transcripts specifically
        if hasattr(YouTubeTranscriptApi, 'list_transcripts'):
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                # Try finding manually created transcripts first (better quality)
                try:
                    t = transcript_list.find_transcript(['hi', 'en', 'en-IN'])
                except:
                    # If specific languages not found, auto-select the first available one
                    t = next(iter(transcript_list))
                
                # Fetch the actual text data
                raw_data = t.fetch()
                transcript_text = " ".join([x['text'] for x in raw_data])
            except Exception as e:
                print(f"List method failed: {e}. Trying fallback...")

        # Method B: Fallback to basic fetch if Method A fails
        if not transcript_text:
             try:
                 # Standard fetch method
                 raw_data = YouTubeTranscriptApi.get_transcript(video_id)
                 transcript_text = " ".join([x['text'] for x in raw_data])
             except:
                 # Last resort: Try 'fetch' directly (handles some library version conflicts)
                 try:
                    raw_data = YouTubeTranscriptApi.fetch(video_id)
                    if isinstance(raw_data, list):
                        transcript_text = " ".join([x.get('text', '') for x in raw_data])
                    else:
                        transcript_text = str(raw_data)
                 except:
                    pass

        # If transcript is still empty, we can't summarize
        if not transcript_text:
            return jsonify({"analysis": "Error: No captions/subtitles found for this video."})

    except Exception as e:
        return jsonify({"analysis": f"Transcript Error: {str(e)}"})

    # 3. SEND TO GOOGLE GEMINI AI
    try:
        print(f"Transcript Length: {len(transcript_text)} characters. Sending to AI...")
        
        # We limit text to 9000 chars to avoid token limits on the free tier
        prompt = f"""
        You are a Fact Checker and Summarizer.
        Analyze the following video transcript.
        Provide a summary in 3 bullet points.
        Language: Hinglish (Mix of Hindi and English) or English.
        
        Transcript: {transcript_text[:9000]}
        """
        
        # We use 'gemini-1.5-flash' because it is fast and free-tier friendly
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        print("✅ Analysis generated successfully!")
        return jsonify({"analysis": response.text})

    except Exception as e:
        error_msg = str(e)
        print(f"❌ AI Error: {error_msg}")
        
        # Handle Rate Limiting (Quota Full)
        if "429" in error_msg:
            return jsonify({"analysis": "⚠️ Server Busy: Google Free Quota Exceeded. Please try again in 2 minutes."})
        
        return jsonify({"analysis": f"AI Error: {error_msg}"})

# Start the Server
if __name__ == '__main__':
    print("--- SERVER STARTED ---")
    print("Listening on http://localhost:5000")
    app.run(debug=True, port=5000)