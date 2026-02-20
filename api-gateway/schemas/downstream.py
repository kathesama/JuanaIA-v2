from typing import List, Optional

from pydantic import BaseModel


class MemoryRecallResponse(BaseModel):
    status: str
    recent: List[str]


class MemoryRememberResponse(BaseModel):
    status: str
    inserted_id: Optional[str] = None


class MemoryResetResponse(BaseModel):
    status: str
    message: Optional[str] = None


class LLMGenerateResponse(BaseModel):
    response: str


class FinanzasProyeccionResponse(BaseModel):
    aporte_mensual_usd: float
    tasa_anual_real: float
    anios: int
    monto_estimado_total_usd: float


class TTSSpeakResponse(BaseModel):
    status: str
    file: Optional[str] = None
    preview: Optional[str] = None
