# Getting Started

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/WARScribe-Core.git
```

## Unit Registration

```python
from warscribe import ActionLog

log = ActionLog()
log.register(unit="Captain in Gravis Armour", id="CPT-01")
log.register(unit="Tactical Squad", id="TAC-01")
```

## Recording Actions

```python
log.record("[MOVE: CPT-01 -> Zone-A]")
log.record("[SHOOT: TAC-01 -> Enemy-01]")
log.record("[CHARGE: CPT-01 -> Enemy-HQ]")
```

## Generate Transcript

```python
print(log.transcript())
```
