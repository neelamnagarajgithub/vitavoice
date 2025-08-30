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



def translate_texts_to_buffer(texts: list[str], target_language: str) -> BytesIO:
    """
    Translates a list of texts to the target language using Murf's translation API,
    and returns the result as a BytesIO buffer.
    """
    api_key = os.getenv("MURF_API_KEY")
    client = Murf(api_key=api_key)
    response = client.text.translate(
        target_language=target_language,
        texts=texts
    )
    buffer = BytesIO()
    buffer.write(str(response).encode('utf-8'))
    buffer.seek(0)
    return buffer