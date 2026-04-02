"""
main.py — Entry point của Voice Assistant
==========================================
Pipeline:
  1. Kiểm tra config (.env)
  2. Load Whisper model
  3. Thu âm từ mic
  4. STT: audio → text
  5. Parser: text → lệnh
  6. Action: gửi email

Chạy: python main.py
"""
import logging
import sys
from pathlib import Path

# ── Setup logging ────────────────────────────────────────────────────────────
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ── Import modules ────────────────────────────────────────────────────────────
from config import settings
from speech.recorder import AudioRecorder
from speech.stt import STTEngine
from parser.command_parser import parse
from actions.email_sender import EmailSender


def run_once():
    """Chạy 1 vòng lệnh: nghe → hiểu → hành động."""

    # ── Bước 0: Validate config ───────────────────────────────────────────
    try:
        settings.validate()
    except EnvironmentError as e:
        print(e)
        sys.exit(1)

    # ── Bước 1: Khởi tạo các component ───────────────────────────────────
    recorder = AudioRecorder()
    stt = STTEngine()
    emailer = EmailSender()

    print("\n" + "=" * 50)
    print("  🎙️  VOICE ASSISTANT — Sẵn sàng")
    print("=" * 50)
    print(f"  Model  : {settings.WHISPER_MODEL} (CPU)")
    print(f"  Thời gian ghi: {settings.RECORD_SECONDS}s")
    print(f"  Email  : {settings.TARGET_EMAIL}")
    print("=" * 50)

    # ── Bước 2: Ghi âm ───────────────────────────────────────────────────
    try:
        audio_path = recorder.record()
    except RuntimeError as e:
        print(e)
        logger.error(e)
        sys.exit(1)

    # ── Bước 3: Speech-to-Text ────────────────────────────────────────────
    text = stt.transcribe(audio_path)
    if not text:
        print("⚠️  Không nhận diện được giọng nói. Thử lại nhé!")
        logger.warning("STT trả về chuỗi rỗng.")
        return

    # ── Bước 4: Parse lệnh ───────────────────────────────────────────────
    command = parse(text)
    if command is None:
        print(f"⚠️  Không hiểu lệnh: '{text}'")
        print("   Thử nói: 'gửi hello world cho gmail của tôi'")
        logger.warning(f"Parse thất bại: '{text}'")
        return

    # ── Bước 5: Thực thi lệnh ────────────────────────────────────────────
    action = command["action"]
    content = command["content"]
    print(f"\n📌 Lệnh nhận ra: {action}")
    print(f"   Nội dung    : {content}")

    if action == "send_email":
        success = emailer.send(content)
        if success:
            print("\n🎉 Hoàn thành!")
        else:
            print("\n💥 Gửi email thất bại. Xem logs/app.log để biết chi tiết.")


def run_loop():
    """Chạy liên tục cho đến khi Ctrl+C."""
    print("\n🔁 Chế độ loop — Nhấn Ctrl+C để thoát\n")
    try:
        while True:
            run_once()
            input("\n⏎  Nhấn Enter để ghi âm tiếp...")
    except KeyboardInterrupt:
        print("\n\n👋 Thoát. Tạm biệt!")


if __name__ == "__main__":
    # Đổi run_once() thành run_loop() nếu muốn chạy liên tục
    run_once()
