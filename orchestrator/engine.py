from __future__ import annotations

from typing import Dict, List, Optional, Protocol

from orchestrator.chain_factory import build_chain
from orchestrator.schemas import AskExtras, OrchestratorResult


class MemoryClient(Protocol):
    def recall(self, *, correlation_id: str, limit: int = 10) -> List[str]:
        ...

    def remember(self, *, correlation_id: str, text: str, role: str, tags: List[str]) -> None:
        ...


class FinanzasClient(Protocol):
    def proyeccion(
        self,
        *,
        correlation_id: str,
        aporte_mensual_usd: float,
        tasa_anual_real: float,
        anios: int,
    ) -> Dict:
        ...


class LLMClient(Protocol):
    def generate(self, *, correlation_id: str, prompt: str) -> str:
        ...


class TTSClient(Protocol):
    def speak(self, *, correlation_id: str, text: str) -> Dict:
        ...


class Orchestrator:
    def __init__(
        self,
        *,
        memory_client: MemoryClient,
        finanzas_client: FinanzasClient,
        llm_client: LLMClient,
        tts_client: TTSClient,
    ) -> None:
        self._memory = memory_client
        self._finanzas = finanzas_client
        self._llm = llm_client
        self._tts = tts_client
        self._chain = build_chain()

    def run_ask_flow(
        self,
        pregunta: str,
        context: List[str],
        extras: Dict,
        *,
        correlation_id: str,
    ) -> OrchestratorResult:
        if context:
            contexto = context
        else:
            contexto = self._memory.recall(correlation_id=correlation_id, limit=10)

        parsed_extras = AskExtras(**extras) if extras else AskExtras()
        proyeccion: Optional[Dict] = None
        if (
            parsed_extras.aporte_mensual_usd is not None
            and parsed_extras.tasa_real_anual is not None
            and parsed_extras.anios is not None
        ):
            proyeccion = self._finanzas.proyeccion(
                correlation_id=correlation_id,
                aporte_mensual_usd=parsed_extras.aporte_mensual_usd,
                tasa_anual_real=parsed_extras.tasa_real_anual,
                anios=parsed_extras.anios,
            )

        prompt = self._chain.build_prompt(
            pregunta=pregunta,
            contexto=contexto,
            proyeccion=proyeccion,
        )

        respuesta_texto = self._llm.generate(correlation_id=correlation_id, prompt=prompt)
        audio = self._tts.speak(correlation_id=correlation_id, text=respuesta_texto)

        self._memory.remember(
            correlation_id=correlation_id,
            text=f"Usuario: {pregunta}",
            role="user",
            tags=["chat"],
        )
        self._memory.remember(
            correlation_id=correlation_id,
            text=f"Juana: {respuesta_texto}",
            role="juana",
            tags=["chat"],
        )

        return OrchestratorResult(
            respuesta_texto=respuesta_texto,
            audio=audio,
            contexto_usado=contexto,
            proyeccion=proyeccion,
        )
