"""
speech/stt.py
Chuyển file WAV thành text dùng faster-whisper.

Model: small (CPU, phù hợp tiếng Việt cơ bản)
"""
import logging
from faster_whisper import WhisperModel

from config import settings

logger = logging.getLogger(__name__)


class STTEngine:
    _instance = None  # Singleton — tránh load model nhiều lần

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        model_name = settings.WHISPER_MODEL
        logger.info(f"⏳ Đang load Whisper model '{model_name}' (CPU)...")
        print(f"⏳ Đang load model '{model_name}'... (lần đầu ~10-30 giây)")
        self.model = WhisperModel(
            model_name,
            device="cpu",
            compute_type="int8",   # int8 nhanh hơn float32 trên CPU
        )
        self._initialized = True
        logger.info(f"✅ Whisper model '{model_name}' đã sẵn sàng")
        print(f"✅ Model sẵn sàng!\n")

    def transcribe(self, audio_path: str) -> str:
        """
        Nhận đường dẫn WAV, trả về text phiên âm.
        - Ngôn ngữ: tiếng Việt (vi)
        - Nếu không nghe rõ: trả về chuỗi rỗng ""
        """
        logger.info(f"🔍 Transcribing: {audio_path}")
        segments, info = self.model.transcribe(
            audio_path,
            language="vi",
            beam_size=5,
            vad_filter=True,          # Lọc đoạn im lặng tự động
            vad_parameters=dict(
                min_silence_duration_ms=500
            ),
        )

        text = " ".join(seg.text.strip() for seg in segments).strip()
        logger.info(f"📝 Kết quả STT: '{text}'")
        print(f"📝 Nhận diện được: '{text}'")
        return text
