from datetime import datetime

usage_log = []

def log_request(user_id: str, tone: str, pitch: float):
    usage_log.append({
        "timestamp": datetime.utcnow(),
        "user": user_id,
        "tone": tone,
        "pitch": pitch
    })

def get_stats():
    return {
        "total_requests": len(usage_log),
        "tones": [entry["tone"] for entry in usage_log]
    }
