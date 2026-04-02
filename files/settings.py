"""
config/settings.py
Load toàn bộ cấu hình từ file .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Gmail
GMAIL_USER: str = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")
TARGET_EMAIL: str = os.getenv("TARGET_EMAIL", "")

# Whisper
WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "small")

# Recording
RECORD_SECONDS: int = int(os.getenv("RECORD_SECONDS", "5"))
SAMPLE_RATE: int = int(os.getenv("SAMPLE_RATE", "16000"))
AUDIO_FILE: str = "audio.wav"

# Logging
LOG_FILE: str = "logs/app.log"

def validate():
    """Kiểm tra config bắt buộc trước khi chạy."""
    missing = []
    if not GMAIL_USER:
        missing.append("GMAIL_USER")
    if not GMAIL_APP_PASSWORD:
        missing.append("GMAIL_APP_PASSWORD")
    if not TARGET_EMAIL:
        missing.append("TARGET_EMAIL")
    if missing:
        raise EnvironmentError(
            f"❌ Thiếu config trong .env: {', '.join(missing)}\n"
            f"   → Sao chép .env.example thành .env và điền đầy đủ."
        )
