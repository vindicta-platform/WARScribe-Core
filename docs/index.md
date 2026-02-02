# WARScribe Core

**The canonical notation engine for Warhammer game actions.**

WARScribe Core provides a human-readable, machine-parseable format for recording gameplay actions. Map units to IDs, record moves, and generate match transcripts.

!!! warning "Scope Clarification"
    WARScribe records **actions only**, not list validation. See [Scope](scope.md) for details.

## What WARScribe Does

| ✅ In Scope | ❌ Out of Scope |
|------------|----------------|
| Unit ID mapping | Point limits |
| Action notation | Legality checks |
| Transcript generation | Loadout rules |

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/WARScribe-Core.git
```

## Quick Example

```python
from warscribe import ActionLog

log = ActionLog()
log.register("Captain", "CPT-01")
log.record("[MOVE: CPT-01 -> Zone-A]")
```

---

[Full Platform](https://vindicta-platform.github.io/mkdocs/)
