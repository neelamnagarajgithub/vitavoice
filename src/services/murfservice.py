import os
from murf import Murf
from io import BytesIO

def stream_tts_to_bytes(text: str, voice_id: str) -> BytesIO:
    """
    Streams TTS audio from Murf and returns as BytesIO buffer.
    """
    api_key = os.getenv("MURF_API_KEY")
    client = Murf(api_key=api_key)
    audio_buffer = BytesIO()
    res = client.text_to_speech.stream(
        text=text,
        voice_id=voice_id
    )
    for audio_chunk in res:
        audio_buffer.write(audio_chunk)
    audio_buffer.seek(0)
    return audio_buffer