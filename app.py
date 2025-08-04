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
