"""
Edition Plugin Architecture for WARScribe-Core.

Provides a pluggable system for supporting different Warhammer 40K editions.
Each edition defines its own phases, action validation, and rules.
"""

from typing import Optional

from warscribe.edition.plugin import (
    EditionPlugin,
    GamePhase,
    PhaseDefinition,
    ValidationResult,
)
from warscribe.edition.registry import EditionRegistry
from warscribe.schema.action import Action, ActionType, ActionResult

__all__ = [
    "EditionPlugin",
    "EditionRegistry",
    "GamePhase",
    "PhaseDefinition",
    "ValidationResult",
    "Action",
    "ActionType",
    "ActionResult",
    "get_edition_registry",
    "register_edition",
    "get_edition",
]


# Global registry singleton
_registry: Optional[EditionRegistry] = None


def get_edition_registry() -> EditionRegistry:
    """Get the global edition registry."""
    global _registry
    if _registry is None:
        _registry = EditionRegistry()
    return _registry


def register_edition(plugin: EditionPlugin, set_default: bool = False) -> None:
    """Register an edition plugin with the global registry."""
    get_edition_registry().register(plugin, set_default)


def get_edition(edition_code: str) -> Optional[EditionPlugin]:
    """Get an edition plugin from the global registry."""
    return get_edition_registry().get(edition_code)
