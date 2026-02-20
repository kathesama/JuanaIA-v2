# JuanaIA v2 Context

## Vision
Build a clean, production-minded architecture that preserves the best behavior from v1 while eliminating monolithic coupling and missing contracts.

## Non-Negotiables
- Timeouts everywhere (default 10s).
- Typed contracts and schema validation for all downstream responses.
- Structured error responses with correlation IDs.
- Logging configured per service.
- LangChain is isolated in `orchestrator/` and not imported in the gateway layer.

## Coding Conventions
- Prefer small modules with explicit interfaces.
- Avoid global side effects in request handlers.
- Validate all external inputs and downstream responses.
- Keep adapters (HTTP clients) separate from use cases.

## Service Responsibilities
- `api-gateway/`: HTTP boundary, request validation, structured errors, and orchestration entrypoint.
- `orchestrator/`: Prompt and flow orchestration, tool wiring, and LLM interaction.
- `services/memory`: Store and recall short-term context.
- `services/llm`: Generate responses for a given prompt.
- `services/finanzas`: Financial projections.
- `services/tts`: Voice output generation.
