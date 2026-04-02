"""
actions/email_sender.py
Gửi email qua Gmail SMTP với App Password.

Cấu hình trong .env:
  GMAIL_USER         → địa chỉ gmail gửi
  GMAIL_APP_PASSWORD → App Password 16 ký tự
  TARGET_EMAIL       → địa chỉ nhận
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


class EmailSender:
    def __init__(self):
        self.sender = settings.GMAIL_USER
        self.password = settings.GMAIL_APP_PASSWORD
        self.recipient = settings.TARGET_EMAIL

    def send(self, content: str) -> bool:
        """
        Gửi email với nội dung `content`.

        Args:
            content: Nội dung cần gửi (từ lệnh thoại)

        Returns:
            True nếu thành công, False nếu thất bại
        """
        subject = f"[Voice Assistant] {datetime.now().strftime('%H:%M %d/%m/%Y')}"
        body = (
            f"Nội dung nhận được từ giọng nói:\n\n"
            f"  {content}\n\n"
            f"---\nGửi tự động bởi Voice Assistant"
        )

        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        try:
            logger.info(f"📧 Đang kết nối SMTP {SMTP_HOST}:{SMTP_PORT}...")
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.recipient, msg.as_string())

            logger.info(f"✅ Email gửi thành công → {self.recipient}")
            print(f"✅ Email đã gửi → {self.recipient}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("❌ Xác thực Gmail thất bại. Kiểm tra App Password trong .env")
            print("❌ Lỗi: App Password không đúng. Kiểm tra lại .env")
            return False

        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP lỗi: {e}")
            print(f"❌ Lỗi SMTP: {e}")
            return False

        except OSError as e:
            logger.error(f"❌ Lỗi kết nối mạng: {e}")
            print(f"❌ Lỗi mạng: {e}")
            return False
