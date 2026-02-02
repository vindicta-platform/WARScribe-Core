# Notation Format

## Action Types

| Action | Format |
|--------|--------|
| Move | `[MOVE: UnitID -> Location]` |
| Shoot | `[SHOOT: UnitID -> TargetID]` |
| Charge | `[CHARGE: UnitID -> TargetID]` |
| Fight | `[FIGHT: UnitID -> TargetID]` |

## Results

```
[SHOOT: TAC-01 -> Enemy-01, Result: 3 wounds]
[CHARGE: CPT-01 -> Enemy-HQ, Success]
```

## Full Transcript

```
=== Turn 1 ===
[MOVE: CPT-01 -> Zone-A]
[SHOOT: TNK-02 -> Enemy-01, Result: 3 wounds]

=== Turn 2 ===
[CHARGE: TAC-03 -> OBJ-1, Success]
```
