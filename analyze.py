from openai import OpenAI
import audio_processing_lib  # dein Modul

async def analyze_audio_frame(audio_bytes: bytes):
    pitch = audio_processing_lib.get_pitch(audio_bytes)
    transcript = audio_processing_lib.transcribe(audio_bytes)
    speed = audio_processing_lib.get_speed(audio_bytes)

    prompt = f"""
    Stimme analysieren:
    Transkript: "{transcript}"
    Tonhöhe: {pitch} Hz
    Tempo: {speed}
    Format:
    {{
      "tone": "...",
      "pitch": "...",
      "speed": "...",
      "confidence": ...
    }}
    """

    response = OpenAI().chat(prompt)
    return response
