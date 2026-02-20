from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OrchestratorResult:
    respuesta_texto: str
    audio: Optional[Dict[str, Any]]
    contexto_usado: List[str]
    proyeccion: Optional[Dict[str, Any]]


@dataclass
class AskExtras:
    aporte_mensual_usd: Optional[float] = None
    tasa_real_anual: Optional[float] = None
    anios: Optional[int] = None
