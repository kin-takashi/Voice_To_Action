PHASE 1 — Core Pipeline (2 ngày)
┌─────────────────────────────────────────────────────┐
│  Mục tiêu: nói → nhận mail (dù code còn thô)        │
│                                                     │
│  Task 1.1: Setup môi trường                         │
│    - venv, requirements.txt                         │
│    - test import faster-whisper                     │
│    - test sounddevice (mic check)                   │
│                                                     │
│  Task 1.2: Audio recording module                   │
│    - Record cố định 5 giây                          │
│    - Save → audio.wav                               │
│    - Kiểm tra waveform                              │
│                                                     │
│  Task 1.3: STT module                               │
│    - Load model medium (tiếng Việt)                 │
│    - Transcribe audio.wav → text                    │
│    - In ra console                                  │
│                                                     │
│  Task 1.4: Email sender                             │
│    - Hardcode subject + body                        │
│    - Gửi qua Gmail SMTP                             │
│    - Xác nhận nhận được mail                        │
│                                                     │
│  Task 1.5: Nối pipeline                             │
│    - main.py chạy end-to-end                        │
│                                                     │
│  ✅ Done khi: nói → mail gửi thành công             │
└─────────────────────────────────────────────────────┘

PHASE 2 — Smart Recording + Parsing (2 ngày)
┌─────────────────────────────────────────────────────┐
│  Mục tiêu: hiểu câu linh hoạt, recording thông minh│
│                                                     │
│  Task 2.1: VAD-based recording                      │
│    - Dùng webrtcvad hoặc silero-vad                 │
│    - Tự dừng khi silence > 1.5s                     │
│    - Max duration = 10s (safeguard)                 │
│                                                     │
│  Task 2.2: Command parser                           │
│    - Pattern chính: "gửi {X} cho gmail (của tôi)"  │
│    - Normalize: lowercase, bỏ dấu câu thừa          │
│    - Fallback: tìm keyword "gửi" + extract phần còn│
│    - Return: {action, content, target} hoặc None    │
│                                                     │
│  Task 2.3: Error handling                           │
│    - Không nhận ra lệnh → thông báo rõ              │
│    - Content rỗng → yêu cầu nói lại                 │
│    - STT confidence thấp → hỏi lại                  │
│                                                     │
│  ✅ Done khi: parse đúng 5/5 test case              │
└─────────────────────────────────────────────────────┘

PHASE 3 — Refactor + Config (2 ngày)
┌─────────────────────────────────────────────────────┐
│  Mục tiêu: code production-ready, dễ mở rộng        │
│                                                     │
│  Task 3.1: Tách module                              │
│    speech/stt.py         → class STTEngine          │
│    speech/recorder.py    → class AudioRecorder      │
│    parser/cmd_parser.py  → class CommandParser      │
│    actions/email.py      → class EmailSender        │
│    config/settings.py    → load .env                │
│                                                     │
│  Task 3.2: .env config                              │
│    GMAIL_USER=...                                   │
│    GMAIL_APP_PASSWORD=...                           │
│    TARGET_EMAIL=...                                 │
│    WHISPER_MODEL=medium                             │
│                                                     │
│  Task 3.3: Logging                                  │
│    - logs/app.log                                   │
│    - Log mỗi bước pipeline                          │
│    - Log lỗi với traceback                          │
│                                                     │
│  Task 3.4: Unit tests                               │
│    - test_parser.py (không cần mic/mail)            │
│    - test_email.py (mock SMTP)                      │
│                                                     │
│  ✅ Done khi: pytest pass, code có docstring        │
└─────────────────────────────────────────────────────┘

PHASE 4 — Optional Enhancements
┌─────────────────────────────────────────────────────┐
│  Task 4.1: Wake word ("Hey assistant")              │
│    - Dùng pvporcupine (local wake word)             │
│                                                     │
│  Task 4.2: TTS feedback                             │
│    - Đọc lại "Đã gửi email chứa {X}"               │
│    - Dùng pyttsx3 (local TTS)                       │
│                                                     │
│  Task 4.3: Mở rộng command                         │
│    - "đặt hẹn giờ X phút"                          │
│    - "nhắc tôi làm X"                              │
│                                                     │
│  Task 4.4: Chuẩn bị IoT                            │
│    - REST API endpoint nhận audio file              │
│    - ESP32 gửi WAV → server xử lý                  │
└─────────────────────────────────────────────────────┘