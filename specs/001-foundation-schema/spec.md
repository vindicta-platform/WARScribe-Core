# Specification: Foundation Schema & Notation Engine (v0.1.0)

**Feature ID:** 001-foundation-schema
**Milestone:** v0.1.0 — Foundation
**Priority:** P0
**Status:** Specified
**Target Date:** Feb 10, 2026

---

## 1. Problem Statement

The Vindicta Platform needs a standardized game notation system for recording,
replaying, and analyzing tabletop wargame actions. Without WARScribe-Core,
each consumer (Primordia-AI, Meta-Oracle, Vindicta-Portal) would create
incompatible transcript formats, making cross-system analysis impossible.

---

## 2. Vision

Create the canonical notation engine for competitive tabletop wargaming:
a JSON Schema-based notation format with a core engine that can serialize,
deserialize, and validate game transcripts.

---

## 3. User Stories

### US-01: Notation Engine — Transcript Serialization

> As a **game tracking application**,
> I want to **serialize a sequence of game actions into a WARScribe transcript**,
> So that **the game can be replayed and analyzed later**.

**Acceptance Criteria:**

- [ ] `Transcript` model contains metadata (date, players, edition) + ordered action list
- [ ] Actions reference Vindicta-Core domain models (Unit, Phase, Action types)
- [ ] Transcript serializes to JSON matching the WARScribe JSON Schema
- [ ] Schema validation provided via `jsonschema` or Pydantic

### US-02: Schema Definition — JSON Schema

> As a **platform developer**,
> I want a **formal JSON Schema for WARScribe notation**,
> So that **third-party tools can validate and generate compatible transcripts**.

**Acceptance Criteria:**

- [ ] JSON Schema v2020-12 defining the complete transcript format
- [ ] Schema covers: transcript metadata, action entries, unit references
- [ ] Schema published as a static file in the package
- [ ] `warscribe_core.schema` module provides programmatic access

### US-03: Action Types — Core Notation

> As the **notation engine**,
> I want to **represent all standard game actions** as typed entries,
> So that **every mechanical event during a game is captured**.

**Acceptance Criteria:**

- [ ] Action types: Move, Shoot, Charge, Fight, StrategyUsed, PhaseTransition
- [ ] Each action entry includes: turn, phase, player, source unit, timestamp
- [ ] Move actions include start/end positions
- [ ] Attack actions include weapon profile, rolls, outcomes

### US-04: Unit Reference System

> As a **transcript consumer**,
> I want to **reference units by stable IDs** within a transcript,
> So that **multiple actions on the same unit are trackable**.

**Acceptance Criteria:**

- [ ] Transcript header includes a unit registry (ID → Unit summary)
- [ ] Action entries reference units by registry ID
- [ ] Unit registry includes faction, name, and starting stats

### US-05: Transcript Validation

> As a **tournament system**,
> I want to **validate a submitted transcript** against the schema,
> So that **I can reject malformed or tampered records**.

**Acceptance Criteria:**

- [ ] `validate_transcript(data)` returns `ValidationResult` (valid/errors)
- [ ] Validates schema compliance + referential integrity (unit IDs exist)
- [ ] Clear error messages for each violation

---

## 4. Functional Requirements

### 4.1 Transcript Model

| Field           | Type                     | Constraints                    |
| --------------- | ------------------------ | ------------------------------ |
| `transcript_id` | `UUID`                   | Auto-generated                 |
| `version`       | `str`                    | Schema version (e.g., "1.0.0") |
| `created_at`    | `datetime`               | UTC timestamp                  |
| `edition`       | `str`                    | Game edition (e.g., "10th")    |
| `players`       | `list[PlayerInfo]`       | Exactly 2                      |
| `unit_registry` | `dict[str, UnitSummary]` | All units in game              |
| `actions`       | `list[ActionEntry]`      | Ordered game actions           |
| `result`        | `GameResult \| None`     | Final outcome                  |

### 4.2 ActionEntry Model

| Field            | Type                | Constraints               |
| ---------------- | ------------------- | ------------------------- |
| `entry_id`       | `UUID`              | Auto-generated            |
| `turn`           | `int`               | >= 1                      |
| `phase`          | `Phase`             | From Vindicta-Core        |
| `player`         | `str`               | Player ID                 |
| `action_type`    | `str`               | Discriminated literal     |
| `source_unit_id` | `str \| None`       | Registry reference        |
| `target_unit_id` | `str \| None`       | Registry reference        |
| `data`           | `dict`              | Type-specific payload     |
| `timestamp`      | `datetime`          | UTC                       |
| `entropy_proofs` | `list[str] \| None` | Proof hashes if available |

### 4.3 JSON Schema

Located at: `schemas/warscribe-transcript-v1.schema.json`
Format: JSON Schema 2020-12
Covers: All models defined in §4.1 and §4.2

### 4.4 Validation API

```python
from warscribe_core import validate_transcript

result = validate_transcript(transcript_json)
if not result.valid:
    for error in result.errors:
        print(f"{error.path}: {error.message}")
```

---

## 5. Non-Functional Requirements

| Category          | Requirement                          |
| ----------------- | ------------------------------------ |
| **Type Safety**   | 100% strict mypy                     |
| **Serialization** | JSON round-trip preserves all fields |
| **Schema**        | Valid JSON Schema 2020-12            |
| **Dependencies**  | Pydantic v2, jsonschema (new)        |
| **Python**        | 3.12+                                |

---

## 6. Out of Scope

- Edition abstraction layer (deferred to v0.2.0)
- Audio/video transcript parsing (WARScribe-Parser scope)
- Replay engine / playback UI

---

## 7. Success Criteria

| Metric           | Target                         |
| ---------------- | ------------------------------ |
| Transcript model | Complete with all fields       |
| JSON Schema      | Valid and covers all types     |
| Validation API   | Schema + referential integrity |
| Test coverage    | > 90%                          |
| Type safety      | Zero mypy errors               |
