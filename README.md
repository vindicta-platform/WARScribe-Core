# WARScribe-Core

Core notation engine for the WARScribe data format.

## Overview

WARScribe-Core provides the canonical implementation of WARScribe notation, the standard format for army list representation in competitive Warhammer.

## Features

- **Notation Engine**: Parse and generate WARScribe format
- **Schema Definition**: Official WARScribe JSON schema
- **Validation**: Army list compliance checking
- **Transformations**: Format conversions

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
