from orchestrator.tools.base import BaseTool, ToolResult


class FinanzasTool(BaseTool):
    name = "finanzas"

    def run(self, **kwargs):
        return ToolResult(ok=False, data={"message": "not implemented"})
