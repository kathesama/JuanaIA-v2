from typing import List, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    pregunta: str = Field(..., min_length=1)
    aporteMensualUSD: Optional[float] = None
    tasaRealAnual: Optional[float] = None
    anios: Optional[int] = None


class AskResponse(BaseModel):
    respuesta: str


class AskResponseFull(BaseModel):
    respuesta_texto: str
    audio: dict
    contexto_usado: List[str]
    proyeccion: Optional[dict]
