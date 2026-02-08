# Implementation Plan: Foundation Schema & Notation Engine (v0.1.0)

**Spec Reference:** [spec.md](./spec.md)
**Feature ID:** 001-foundation-schema

---

## Goal

Create the WARScribe-Core notation engine with transcript models, JSON Schema,
and validation API.

---

## Proposed Changes

### Package Structure

```
src/warscribe_core/
├── __init__.py
├── models/
│   ├── __init__.py        # Re-exports
│   ├── transcript.py      # Transcript, PlayerInfo, UnitSummary, GameResult
│   ├── actions.py         # ActionEntry with type-specific payloads
│   └── registry.py        # UnitRegistry with lookup helpers
├── schema/
│   ├── __init__.py        # load_schema(), get_schema_path()
│   └── warscribe-transcript-v1.schema.json
├── validation/
│   ├── __init__.py        # validate_transcript()
│   ├── schema_validator.py    # JSON Schema validation
│   └── integrity_validator.py # Referential integrity checks
└── engine/
    ├── __init__.py
    └── notation.py        # NotationEngine: build/append/finalize transcripts
```

### Key Files

#### [NEW] models/transcript.py
- `PlayerInfo`, `UnitSummary`, `GameResult`, `Transcript` Pydantic models
- Extends Vindicta-Core `VindictaModel` base class
- `Transcript.to_json()` / `Transcript.from_json()` convenience methods

#### [NEW] models/actions.py
- `ActionEntry` with discriminated `action_type` field
- Type-specific data payloads as typed dicts
- Entropy proof chain attachment

#### [NEW] schema/warscribe-transcript-v1.schema.json
- JSON Schema 2020-12 definition matching all Pydantic models
- Auto-validated against Pydantic schema generation for consistency

#### [NEW] validation/schema_validator.py
- Wraps `jsonschema.validate()` with friendly error reporting
- Returns `ValidationResult` with path-specific error messages

#### [NEW] validation/integrity_validator.py
- Checks unit ID references against registry
- Checks phase ordering within turns

#### [NEW] engine/notation.py
- `NotationEngine` class for building transcripts
- `begin_game()` → `add_action()` → `finalize()` pattern

### Tests

#### [NEW] tests/test_transcript.py — Model creation, serialization
#### [NEW] tests/test_schema.py — Schema loading, validation
#### [NEW] tests/test_validation.py — Schema + integrity checks
#### [NEW] tests/test_notation_engine.py — Full transcript building

---

## Verification Plan

```powershell
uv run pytest tests/ -v
uv run mypy src/warscribe_core/ --strict
uv run python -c "from warscribe_core import validate_transcript; print('OK')"
```
