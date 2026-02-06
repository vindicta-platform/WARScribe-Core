# WARScribe-Core Constraints

> Critical rules agents MUST follow when modifying this repository.

## ⛔ Hard Constraints

1. **GRAMMAR.md is Canonical** - All notation changes MUST update GRAMMAR.md first
2. **Edition Agnostic Core** - No hardcoded edition-specific rules in core parser
3. **All Editions via Plugins** - Edition specifics go in `plugins/` only
4. **100% Test Coverage** - New features require tests before merge

## 📜 Notation Invariants

These notation rules are IMMUTABLE:

```
# Phase markers
COMMAND | MOVEMENT | SHOOTING | CHARGE | FIGHT | MORALE

# Action format
[UNIT] -> [ACTION] -> [TARGET] : [RESULT]

# Dice notation
XdY+Z (e.g., 2d6+3)
```

## ⚠️ Schema Compatibility

### AST Node Types
All AST nodes must include:
- `type: string` - Node type identifier
- `location: {line, column}` - Source position
- `children: Node[]` - Child nodes (if applicable)

### Domain Model Contracts
- `Action` - Atomic game action
- `Phase` - Collection of actions in a phase
- `Turn` - Collection of phases
- `Transcript` - Full game record

## 🔒 Validation Rules

1. Unit names must exist in active edition roster
2. Actions must be valid for the current phase
3. Dice expressions must be syntactically valid
4. Turn sequence must follow edition rules

## 🧪 Testing Requirements

Before merging:
- [ ] `pytest` passes with 100% coverage
- [ ] Grammar conformance suite passes
- [ ] Property-based tests pass (Hypothesis)
- [ ] Run `verify-warscribe` skill if available
