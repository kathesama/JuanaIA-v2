# ADR 0001: Isolate LangChain Behind Orchestrator Interface

## Status
Accepted

## Context
The gateway must remain stable and focused on HTTP concerns. LangChain changes frequently and introduces heavy dependencies and patterns that should not leak into the edge layer.

## Decision
All LangChain wiring lives in `orchestrator/chain_factory.py` and is accessed via the `Orchestrator` interface. The gateway depends only on the orchestrator interface and does not import LangChain directly.

## Consequences
- The gateway remains lightweight and stable.
- LangChain can be upgraded or replaced with minimal impact.
- Tests can mock the orchestrator without LangChain installed.
