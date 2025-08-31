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
from dotenv import load_dotenv
from pymongo import MongoClient
from elevenlabs.client import ElevenLabs

load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vitavoice"]
audio_col = db["audio_files"]

# ElevenLabs setup
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def store_audio_in_mongo(username: str, audio_file) -> str:
    """
    Stores an uploaded audio file (file-like object) in MongoDB.
    Returns the inserted document's ID as a string.
    """
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
    Returns the audio bytes.
    """
    from bson import ObjectId
    doc = audio_col.find_one({"_id": ObjectId(audio_id)})
    if doc:
        return doc["audio"]
    else:
        return None

def speech_to_text(audio_id) -> str:
    """
    Retrieves audio from MongoDB and transcribes it using ElevenLabs STT API.
    """
    from io import BytesIO
    audio_bytes = get_audio_from_mongo(audio_id)
    if not audio_bytes:
        print("No audio found for this ID.")
        return ""
    audio_data = BytesIO(audio_bytes)
    transcription = elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1",
        tag_audio_events=False,
        language_code="eng",
        diarize=True,
    )
    print(transcription)
    if isinstance(transcription, dict) and "text" in transcription:
        return transcription["text"]
    elif hasattr(transcription, "text"):
        return transcription.text
    else:
        return str(transcription)