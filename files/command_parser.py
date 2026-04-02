"""
parser/command_parser.py
Phân tích câu lệnh tiếng Việt và trích xuất thông tin.

Hỗ trợ Pattern:
  - "gửi {content} cho gmail của tôi"
  - "gửi {content} cho gmail"
  - "gửi {content} tới gmail"
  - "send {content} cho gmail"   (fallback tiếng Anh)

Returns:
  dict  → {"action": "send_email", "content": "..."}
  None  → không nhận ra lệnh
"""
import re
import logging

logger = logging.getLogger(__name__)

# Các từ không được là nội dung duy nhất (stop words)
_STOP_WORDS = {"cho", "tới", "toi", "den", "đến", "to", "my"}

# ── Pattern chính ────────────────────────────────────────────────────────────
_SEND_PATTERNS = [
    # Chính xác nhất — "gửi X cho gmail của tôi"
    r"(?:gửi|goi|gui)\s+(.+?)\s+(?:cho|tới|toi|den)\s+gmail(?:\s+của\s+tôi)?",
    # Fallback nhẹ — "gửi X gmail"
    r"(?:gửi|goi|gui)\s+(.+?)\s+gmail",
    # Tiếng Anh fallback
    r"send\s+(.+?)\s+(?:to\s+)?(?:my\s+)?gmail",
]

_COMPILED = [re.compile(p, re.IGNORECASE | re.UNICODE) for p in _SEND_PATTERNS]


def parse(text: str) -> dict | None:
    """
    Phân tích text, trả về dict lệnh hoặc None.

    Args:
        text: Câu lệnh thô từ STT (tiếng Việt)

    Returns:
        {"action": "send_email", "content": str}  hoặc  None
    """
    if not text:
        logger.warning("⚠️  Text rỗng, không parse được.")
        return None

    normalized = _normalize(text)
    logger.info(f"🔍 Parse: '{normalized}'")

    for pattern in _COMPILED:
        match = pattern.search(normalized)
        if match:
            content = match.group(1).strip()
            # Loại bỏ trường hợp content chỉ là stop word
            if not content or content.lower() in _STOP_WORDS:
                logger.warning("⚠️  Content rỗng hoặc chỉ là stop word.")
                return None
            result = {"action": "send_email", "content": content}
            logger.info(f"✅ Parse OK: {result}")
            return result

    logger.warning(f"❌ Không nhận ra lệnh từ: '{normalized}'")
    return None


def _normalize(text: str) -> str:
    """Chuẩn hóa text: lowercase, bỏ ký tự thừa."""
    text = text.lower().strip()
    text = re.sub(r"[,\.!?]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text
