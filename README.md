# 🗣️ VoiceCheck API

Dieses Projekt stellt eine einfache, Cloud-basierte API zur Verfügung, mit der Audio-Dateien automatisch analysiert und ausgewertet werden können. Ziel ist es, eine flexible und schnelle Lösung zur Sprachüberprüfung bereitzustellen – ideal für mobile Apps, Webservices und andere digitale Anwendungen.

---

## 🚀 Funktionen

- 🔍 Sprachdateien hochladen & automatisch analysieren
- ✅ Rückmeldung über Klarheit, Lautstärke und Verständlichkeit
- 🧠 Optional: KI-gestützte Einschätzung der Emotion im Tonfall
- 🔄 JSON-basierte API-Response für einfache Integration

---

## 🛠️ Technologien

- **Python** (FastAPI)
- **Render** für Hosting
- **SpeechRecognition** & **pydub** zur Audioverarbeitung
- `requirements.txt` für alle Abhängigkeiten

---

## 📦 Installation & Nutzung

```bash
# 1. Repository klonen
git clone https://github.com/dein-benutzername/timnet-voicecheck-api.git
cd timnet-voicecheck-api

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Server starten
uvicorn app:app --reload
