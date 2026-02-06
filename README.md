# WARScribe-Core

Core notation engine for the WARScribe data format.

## Overview

WARScribe-Core provides the canonical implementation of WARScribe notation, the standard format for army list representation in competitive Warhammer.

## Features

- **Notation Engine**: Parse and generate WARScribe format
- **Schema Definition**: Official WARScribe JSON schema
- **Transformations**: Format conversions
- **Edition Plugins**: Extensible game edition support

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

## Edition Plugin System

WARScribe-Core uses a pluggable architecture for supporting different Warhammer 40K editions. Each edition defines its own phases, action validation, and game rules.

### EditionPlugin Interface

To create a custom edition plugin, extend the `EditionPlugin` abstract base class:

| Property/Method | Type | Description |
|-----------------|------|-------------|
| `edition_name` | `str` | Human-readable edition name (e.g., "Warhammer 40,000 10th Edition") |
| `edition_code` | `str` | Short identifier used for registration (e.g., "10th", "9th") |
| `phases` | `Sequence[PhaseDefinition]` | Ordered sequence of game phases for this edition |
| `validate_action(action, game_state)` | `ValidationResult` | Validates an action against edition rules |

### Creating an Edition Plugin

```python
from typing import Any, Optional, Sequence

from warscribe.edition import (
    EditionPlugin,
    GamePhase,
    PhaseDefinition,
    ValidationResult,
)
from warscribe.schema.action import Action, ActionType


class NinthEditionPlugin(EditionPlugin):
    """Example plugin for 9th Edition."""

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
                allowed_actions=[ActionType.STRATAGEM, ActionType.ABILITY],
            ),
            PhaseDefinition(
                name=GamePhase.MOVEMENT,
                display_name="Movement Phase",
                order=1,
                allowed_actions=[ActionType.MOVE, ActionType.ADVANCE],
            ),
            PhaseDefinition(
                name=GamePhase.PSYCHIC,
                display_name="Psychic Phase",
                order=2,
                allowed_actions=[ActionType.ABILITY],
            ),
            # ... additional phases
        ]

    def validate_action(
        self, action: Action, game_state: Optional[Any] = None
    ) -> ValidationResult:
        # Validate action against 9th Edition rules
        if not self.is_action_allowed_in_phase(action.action_type, action.phase):
            return ValidationResult.failure(
                f"Action '{action.action_type.value}' not allowed in '{action.phase}'."
            )
        return ValidationResult.success()
```

### Supporting Types

- **`PhaseDefinition`**: Defines a game phase with name, order, allowed actions, and optional description
- **`ValidationResult`**: Result object with `is_valid`, `errors`, and `warnings` fields
- **`GamePhase`**: Enum of standard phases (COMMAND, MOVEMENT, PSYCHIC, SHOOTING, CHARGE, FIGHT, MORALE)

### EditionRegistry

Register and retrieve edition plugins using the global registry:

```python
from warscribe.edition import register_edition, get_edition, get_edition_registry

# Register a custom plugin
register_edition(NinthEditionPlugin(), set_default=False)

# Retrieve a registered plugin
edition = get_edition("9th")

# List all available editions
registry = get_edition_registry()
print(registry.available_editions)  # ["10th", "9th"]
```

### Reference Implementation

See [`TenthEditionPlugin`](src/warscribe/edition/tenth.py) for a complete reference implementation of the 10th Edition rules.

## Related Repositories

| Repository | Relationship |
|------------|-------------|
| [WARScribe-Parser](https://github.com/vindicta-platform/WARScribe-Parser) | High-level parser |
| [WARScribe-CLI](https://github.com/vindicta-platform/WARScribe-CLI) | CLI tools |

## License

MIT License - See [LICENSE](./LICENSE) for details.
