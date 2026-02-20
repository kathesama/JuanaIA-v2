from typing import Optional

from orchestrator.engine import Orchestrator
from orchestrator.schemas import OrchestratorResult


class AskUseCase:
    def __init__(self, orchestrator: Orchestrator) -> None:
        self._orchestrator = orchestrator

    def execute(
        self,
        *,
        pregunta: str,
        aporte_mensual_usd: Optional[float],
        tasa_real_anual: Optional[float],
        anios: Optional[int],
        full: bool,
        correlation_id: str,
    ) -> OrchestratorResult:
        extras = {
            "aporte_mensual_usd": aporte_mensual_usd,
            "tasa_real_anual": tasa_real_anual,
            "anios": anios,
        }
        return self._orchestrator.run_ask_flow(
            pregunta=pregunta,
            context=[],
            extras=extras,
            correlation_id=correlation_id,
        )
