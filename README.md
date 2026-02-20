 JuanaIA v2

## Architecture
- `api-gateway/`: FastAPI edge service exposing public endpoints and enforcing contracts, timeouts, and structured errors.
- `orchestrator/`: Coordinates the ask flow and isolates LangChain wiring behind a stable interface.
- `services/`: Downstream services (memory, llm, finanzas, tts). Each is a minimal FastAPI service.
- `common/`: Shared config, logging, error handling, and HTTP client wrapper.

## Run (Docker Compose)
```bash
cd D:\projects\ia\JuanaIA
docker compose up -d --build
```

Gateway:
- `http://localhost:8080/health`

## Run Tests
```bash
cd D:\projects\ia\JuanaIA
pip install -r requirements-dev.txt
pytest
```

## Add A New Tool To The Orchestrator
1. Create a tool in `orchestrator/tools/` implementing `BaseTool`.
2. Wire it in `orchestrator/chain_factory.py` (or in the orchestrator flow) with a clear interface.
3. Add contract tests for any new downstream responses.
4. Update the README with the new tool description and required env/config.
