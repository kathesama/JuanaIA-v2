from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    ok: bool
    data: Dict[str, Any]


class BaseTool:
    name: str = ""

    def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
