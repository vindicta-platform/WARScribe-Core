# WARScribe-Core

Core notation engine for the WARScribe data format.

## Overview

WARScribe-Core provides the canonical implementation of WARScribe notation, the standard format for army list representation in competitive Warhammer.

## Features

- **Notation Engine**: Parse and generate WARScribe format
- **Schema Definition**: Official WARScribe JSON schema
- **Transformations**: Format conversions

## Edition Plugin System

WARScribe-Core uses a pluggable architecture to support different Warhammer editions (9th, 10th, 11th, Horus Heresy). Each edition implements the `EditionPlugin` interface to define its unique phases, rules, and action validation.

### EditionPlugin Interface

The abstract `EditionPlugin` class defines the contract for edition implementations:

| Property/Method | Return Type | Description |
|----------------|-------------|-------------|
| `edition_name` | `str` | Human-readable name (e.g., "Warhammer 40,000 10th Edition") |
| `edition_code` | `str` | Short identifier (e.g., "10th", "9th", "HH") |
| `phases` | `Sequence[PhaseDefinition]` | Ordered list of game phases |
| `validate_action(action, game_state)` | `ValidationResult` | Validate an action against edition rules |

Helper methods are provided: `get_phase()`, `get_phase_order()`, `get_next_phase()`, `is_action_allowed_in_phase()`.

### EditionRegistry

The `EditionRegistry` manages plugin discovery and access:

```python
from warscribe.edition import EditionRegistry, get_edition_registry, register_edition
from warscribe.edition.tenth import TenthEditionPlugin

# Register an edition
registry = get_edition_registry()
register_edition(TenthEditionPlugin(), set_default=True)

# Retrieve an edition
edition = registry.get("10th")
print(edition.edition_name)  # "Warhammer 40,000 10th Edition"

# List available editions
print(registry.available_editions)  # ["10th"]
```

### Creating a Custom Edition

To support a new edition, subclass `EditionPlugin`:

```python
from typing import Any, Optional, Sequence
from warscribe.edition import (
    EditionPlugin, GamePhase, PhaseDefinition, ValidationResult
)
from warscribe.schema.action import Action, ActionType

class NinthEditionPlugin(EditionPlugin):
    @property
    def edition_name(self) -> str:
        return "Warhammer 40,000 9th Edition"
    
    @property
    def edition_code(self) -> str:
        return "9th"
    
    @property
    def phases(self) -> Sequence[PhaseDefinition]:
        return [
            PhaseDefinition(
                name=GamePhase.COMMAND,
                display_name="Command Phase",
                order=0,
                allowed_actions=[ActionType.STRATAGEM],
            ),
            PhaseDefinition(
                name=GamePhase.MOVEMENT,
                display_name="Movement Phase",
                order=1,
                allowed_actions=[ActionType.MOVE, ActionType.ADVANCE],
            ),
            PhaseDefinition(
                name=GamePhase.PSYCHIC,  # 9th has Psychic phase!
                display_name="Psychic Phase",
                order=2,
                allowed_actions=[ActionType.ABILITY],
            ),
            # ... additional phases
        ]
    
    def validate_action(
        self, action: Action, game_state: Optional[Any] = None
    ) -> ValidationResult:
        # Validate action type allowed in phase
        if not self.is_action_allowed_in_phase(action.action_type, action.phase):
            return ValidationResult.failure(
                f"Action '{action.action_type.value}' not allowed in '{action.phase}'."
            )
        return ValidationResult.success()
```

### Reference Implementation

See [`TenthEditionPlugin`](src/warscribe/edition/tenth.py) for a complete reference implementation of the 10th Edition rules.

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/WARScribe-Core.git
```

Or clone locally:

```bash
git clone https://github.com/vindicta-platform/WARScribe-Core.git
cd WARScribe-Core
uv pip install -e .
```

## Related Repositories

| Repository | Relationship |
|------------|-------------|
| [WARScribe-Parser](https://github.com/vindicta-platform/WARScribe-Parser) | High-level parser |
| [WARScribe-CLI](https://github.com/vindicta-platform/WARScribe-CLI) | CLI tools |

## License

MIT License - See [LICENSE](./LICENSE) for details.
