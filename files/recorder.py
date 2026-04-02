"""
speech/recorder.py
Thu âm từ microphone và lưu ra file WAV.

Phase 1: Fixed-duration recording (đơn giản, đáng tin cậy)
Phase 2: Sẽ nâng cấp lên VAD-based (tự dừng khi im lặng)
"""
import logging
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from config import settings

logger = logging.getLogger(__name__)


class AudioRecorder:
    def __init__(
        self,
        sample_rate: int = settings.SAMPLE_RATE,
        duration: int = settings.RECORD_SECONDS,
        output_file: str = settings.AUDIO_FILE,
    ):
        self.sample_rate = sample_rate
        self.duration = duration
        self.output_file = output_file

    def record(self) -> str:
        """
        Thu âm trong `duration` giây từ mic mặc định.
        Returns: đường dẫn file WAV đã lưu.
        Raises: RuntimeError nếu không tìm thấy mic.
        """
        logger.info(f"🎤 Bắt đầu thu âm {self.duration} giây...")
        print(f"\n🎤 Đang nghe... ({self.duration} giây)")

        try:
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
            )
            sd.wait()  # Đợi cho đến khi xong
        except sd.PortAudioError as e:
            raise RuntimeError(f"❌ Lỗi microphone: {e}") from e

        write(self.output_file, self.sample_rate, recording)
        logger.info(f"✅ Đã lưu audio → {self.output_file}")
        print(f"✅ Ghi âm xong → {self.output_file}")
        return self.output_file

    @staticmethod
    def list_devices():
        """In danh sách thiết bị audio (debug helper)."""
        print(sd.query_devices())
