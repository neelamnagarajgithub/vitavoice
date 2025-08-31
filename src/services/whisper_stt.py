# # services/whisper_stt.py
# import whisper
# from tempfile import NamedTemporaryFile

# # Load the model globally (choose "base" or "small" for faster CPU inference)
# model = whisper.load_model("medium")

# def speech_to_text(audio_file) -> str:
#     """
#     Convert audio (BytesIO, raw bytes, or file-like object) into text using Whisper.
#     """
#     # Handle BytesIO vs file-like vs raw bytes
#     audio_bytes = audio_file.read() if hasattr(audio_file, "read") else audio_file

#     with NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
#         temp_audio.write(audio_bytes)
#         temp_audio.flush()
#         result = model.transcribe(temp_audio.name, fp16=False)  # fp16=False for CPU stability
#         return result["text"].strip()


# src/utils/transcribe.py
# from tempfile import NamedTemporaryFile
# from faster_whisper import WhisperModel

# model = WhisperModel("small", device="cpu", compute_type="int8")

# def speech_to_text(audio_file) -> str:
#     """
#     Convert audio (BytesIO, raw bytes, or file-like object) into text using faster-whisper.
#     Also prints the recognized text to the terminal.
#     """
#     audio_bytes = audio_file.read() if hasattr(audio_file, "read") else audio_file
#     print(f"[DEBUG] audio_bytes length: {len(audio_bytes)}")
#     with NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
#         temp_audio.write(audio_bytes)
#         temp_audio.flush()
#         segments, info = model.transcribe(temp_audio.name)
#         text = " ".join([segment.text for segment in segments]).strip()
#         print(f"[Whisper STT] Recognized text: {text}")  # <-- Print to terminal
#         return text

import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vitavoice"]
audio_col = db["audio_files"]

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
STT_URL = "https://api.elevenlabs.io/v1/speech-to-text"

def store_audio_in_mongo(username: str, audio_file) -> str:
    audio_bytes = audio_file.read() if hasattr(audio_file, "read") else audio_file
    doc = {
        "username": username,
        "audio": audio_bytes,
        "content_type": "audio/mp3"
    }
    result = audio_col.insert_one(doc)
    return str(result.inserted_id)

def get_audio_from_mongo(audio_id):
    """
    Retrieves audio binary data from MongoDB by document ID.
    Returns the audio bytes and local path.
    """
    from bson import ObjectId
    doc = audio_col.find_one({"_id": ObjectId(audio_id)})
    if doc:
        return doc["audio"], doc.get("local_path")
    else:
        return None, None

def speech_to_text(audio_id) -> str:
    audio_bytes, _ = get_audio_from_mongo(audio_id)
    if not audio_bytes:
        print("No audio found for this ID.")
        return ""
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    files = {
        "file": ("audio.mp3", audio_bytes, "audio/mp3")
    }
    data = {
        "model_id": "scribe_v1"
    }
    response = requests.post(STT_URL, headers=headers, data=data, files=files, timeout=60)
    result = response.json()
    if result.get('language_code') == 'eng':
        return result.get('text', '')
    else:
        print('No English content found.')
        return ""