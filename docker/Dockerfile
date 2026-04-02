FROM python:3.10-slim

WORKDIR /VOICE_TO_ACTION

COPY /requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m","App.main"]