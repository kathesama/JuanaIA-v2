from schemas.downstream import (
    FinanzasProyeccionResponse,
    LLMGenerateResponse,
    MemoryRecallResponse,
    TTSSpeakResponse,
)


def test_memory_recall_schema():
    data = {"status": "ok", "recent": ["a", "b"]}
    parsed = MemoryRecallResponse.model_validate(data)
    assert parsed.recent == ["a", "b"]


def test_llm_schema():
    data = {"response": "hola"}
    parsed = LLMGenerateResponse.model_validate(data)
    assert parsed.response == "hola"


def test_finanzas_schema():
    data = {
        "aporte_mensual_usd": 10.0,
        "tasa_anual_real": 0.05,
        "anios": 2,
        "monto_estimado_total_usd": 252.0,
    }
    parsed = FinanzasProyeccionResponse.model_validate(data)
    assert parsed.monto_estimado_total_usd == 252.0


def test_tts_schema():
    data = {"status": "generated", "file": "/tmp/a.wav", "preview": "x"}
    parsed = TTSSpeakResponse.model_validate(data)
    assert parsed.status == "generated"
