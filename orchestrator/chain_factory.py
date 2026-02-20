from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PromptChain:
    system_prompt: str

    def build_prompt(self, *, pregunta: str, contexto: List[str], proyeccion: Optional[Dict]) -> str:
        prompt = (
            self.system_prompt
            + "\n\n=== CONTEXTO RECIENTE ===\n"
            + "\n".join(contexto)
            + "\n\n=== PREGUNTA ACTUAL ===\n"
            + pregunta
        )
        if proyeccion:
            prompt += "\n\n=== DATOS FINANCIEROS CALCULADOS ===\n" + str(proyeccion)
        return prompt


DEFAULT_SYSTEM_PROMPT = """
Eres Juana, una asistente personal privada.
Responde con calidez, claridad y sin vueltas.
""".strip()


def build_chain() -> PromptChain:
    """
    LangChain wiring belongs here. This placeholder keeps the gateway isolated.
    Replace this with a LangChain prompt/template pipeline when ready.
    """
    return PromptChain(system_prompt=DEFAULT_SYSTEM_PROMPT)
