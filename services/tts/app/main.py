from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="juana-tts")


class SpeakRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "tts", "mode": "stub"}


@app.post("/speak")
def speak(req: SpeakRequest):
    return {"status": "generated", "file": "/tmp/fake_audio.wav", "preview": "(voz simulada) " + req.text}
