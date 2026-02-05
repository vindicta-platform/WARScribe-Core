# WARScribe-Core

Core notation engine for the WARScribe data format.

## Overview

WARScribe-Core provides the canonical implementation of WARScribe notation, the standard format for army list representation in competitive Warhammer.

## Features

- **Notation Engine**: Parse and generate WARScribe format
- **Schema Definition**: Official WARScribe JSON schema
- **Transformations**: Format conversions
- **Edition Plugin System**: Pluggable edition-specific rule implementations

## Edition Plugin System

WARScribe-Core uses a plugin architecture to support multiple Warhammer editions (10th, 11th, Horus Heresy) through a common `EditionPlugin` interface.

### Plugin Interface

All edition plugins must implement:

```python
from warscribe.edition import EditionPlugin

class CustomEditionPlugin(EditionPlugin):
    @property
    def edition_name(self) -> str:
        """Edition identifier (e.g., '10th', '11th')."""
        return "11th"
    
    @property
    def version(self) -> str:
        """Edition version string (e.g., '11.0.0')."""
        return "11.0.0"
    
    def validate_movement(self, unit: Unit, distance: int) -> bool:
        """Check if unit movement is legal."""
        return distance <= unit.movement
    
    def validate_action(self, action: Action) -> tuple[bool, Optional[str]]:
        """Validate game action against edition rules.
        
        Returns:
            (is_valid, error_message) tuple
        """
        # Custom validation logic
        return (True, None)
    
    def calculate_hit_rolls(
        self, weapon_skill: int, target_toughness: int, modifiers: dict
    ) -> int:
        """Calculate required hit roll (2-6)."""
        # Custom hit calculation
        return weapon_skill
```

### Using Plugins

```python
from warscribe.edition.tenth import TenthEditionPlugin

plugin = TenthEditionPlugin()
print(plugin.edition_name)  # "10th"
print(plugin.version)       # "10.1.0"

# Validate movement
is_valid = plugin.validate_movement(unit, distance=6)

# Validate action
valid, error = plugin.validate_action(action)
if not valid:
    print(f"Invalid action: {error}")
```

### Reference Implementation

See [`TenthEditionPlugin`](src/warscribe/edition/tenth.py) for the canonical 10th Edition implementation (Pariah Nexus season).

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
