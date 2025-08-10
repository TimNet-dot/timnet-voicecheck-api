from flask import Flask, request, jsonify
import whisper
import openai
import tempfile

app = Flask(__name__)
model = whisper.load_model("base")
openai.api_key = "DEIN_API_KEY"  # 🔐 API-Key hier eintragen

@app.route("/analyze", methods=["POST"])
def analyze_audio():
    audio_file = request.files["audio"]
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        audio_file.save(temp_audio.name)
        result = model.transcribe(temp_audio.name)

    transcript = result["text"]

    prompt = f"""
Analysiere den folgenden transkribierten Text. Bewerte die Glaubwürdigkeit und gib eine Einschätzung auf einer Skala von 0 bis 100, wobei 0 für 'sicher gelogen' und 100 für 'absolut glaubwürdig' steht.

Antwortformat (JSON):
{{"score": INT, "verdict": STRING, "reasoning": STRING}}

Text: '{transcript}'
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    reply_text = response.choices[0].message.content

    return jsonify({
        "transcript": transcript,
        "gpt_analysis": reply_text
    })

if __name__ == "__main__":
    app.run(debug=True)
from live_analysis import analyze_live_audio
@app.post("/live")
async def live_endpoint(request: Request):
    return await analyze_live_audio(request)
from auth import verify_api_key

@app.post("/analyze")
async def analyze(request: Request):
    await verify_api_key(request)
    # ...weiter mit Analyse
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = get_openapi(
        title="TimNet VoiceCheck API",
        version="2.0",
        description="Analyse von Stimme, Tonfall und Wahrheit",
        routes=app.routes,
    )
    return app.openapi_schema

app.openapi = custom_openapi
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import asyncio
import uvicorn

app = FastAPI()

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    # Simuliere asynchrone Verarbeitung
    audio_bytes = await file.read()

    # Beispiel: Async GPT-Call oder Analyse
    result = await process_audio_async(audio_bytes)
from fastapi import FastAPI, UploadFile, File
from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.redis import RedisBackend
from redis import Redis
import hashlib

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = Redis(host="localhost", port=6379, db=0)
    FastAPICache.init(RedisBackend(redis), prefix="voicecheck")

def hash_audio(audio_bytes: bytes) -> str:
    return hashlib.md5(audio_bytes).hexdigest()

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    audio_hash = hash_audio(audio_bytes)

    # Check cache
    cached = await FastAPICache.get(audio_hash)
    if cached:
        return {"cached": True, "analysis": cached}

    # Simulierte Analyse
    result = {"clarity": "clear", "emotion": "neutral"}

    # Speichern im Cache
    await FastAPICache.set(audio_hash, result, expire=3600)

    return {"cached": False, "analysis": result}

    return JSONResponse(content={"analysis": result})

async def process_audio_async(audio_bytes):
    # Hier könnte z. B. ein GPT-Call oder eine KI-Analyse stehen
    await asyncio.sleep(0.5)  # Simulierter Delay
    return {"clarity": "clear", "emotion": "neutral"}
gunicorn app:app --workers 4 --threads 2 --timeout 60 --bind 0.0.0.0:8000
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
