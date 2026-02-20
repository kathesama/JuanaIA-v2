from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="juana-llm")


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "llm", "mode": "stub"}


@app.post("/generate")
def generate(req: GenerateRequest):
    return {"response": f"(stubbed) {req.prompt[:200]}"}
