"""
Edition Plugin Architecture for WARScribe-Core.

Provides a pluggable system for supporting different Warhammer 40K editions.
Each edition defines its own phases, action validation, and rules.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, Sequence

from warscribe.schema.action import Action, ActionType, ActionResult


class GamePhase(str, Enum):
    """
    Standard game phases.
    
    Edition plugins can define additional phases or skip phases.
    """
    COMMAND = "command"
    MOVEMENT = "movement"
    PSYCHIC = "psychic"
    SHOOTING = "shooting"
    CHARGE = "charge"
    FIGHT = "fight"
    MORALE = "morale"


@dataclass
class PhaseDefinition:
    """Definition of a game phase for an edition."""
    
    name: str
    display_name: str
    order: int
    allowed_actions: list[ActionType]
    description: str = ""
    is_optional: bool = False


@dataclass 
class ValidationResult:
    """Result of validating an action."""
    
    is_valid: bool
    errors: list[str]
    warnings: list[str]
    
    @classmethod
    def success(cls) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, errors=[], warnings=[])
    
    @classmethod
    def failure(cls, *errors: str) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, errors=list(errors), warnings=[])
    
    def add_warning(self, warning: str) -> None:
        """Add a warning to the result."""
        self.warnings.append(warning)


class EditionPlugin(ABC):
    """
    Abstract base class for edition plugins.
    
    Each supported edition (e.g., 9th, 10th) implements this interface
    to define its unique rules, phases, and action validation.
    
    Example:
        class TenthEditionPlugin(EditionPlugin):
            @property
            def edition_name(self) -> str:
                return "Warhammer 40,000 10th Edition"
            
            @property  
            def edition_code(self) -> str:
                return "10th"
    """
    
    @property
    @abstractmethod
    def edition_name(self) -> str:
        """Human-readable edition name."""
        pass
    
    @property
    @abstractmethod
    def edition_code(self) -> str:
        """Short edition identifier (e.g., '10th', '9th')."""
        pass
    
    @property
    @abstractmethod
    def phases(self) -> Sequence[PhaseDefinition]:
        """
        Return the ordered sequence of game phases for this edition.
        
        The order in the sequence determines the phase order in a turn.
        """
        pass
    
    def get_phase(self, phase_name: str) -> Optional[PhaseDefinition]:
        """Get a phase definition by name."""
        for phase in self.phases:
            if phase.name == phase_name:
                return phase
        return None
    
    def get_phase_order(self, phase_name: str) -> int:
        """Get the order index of a phase (-1 if not found)."""
        phase = self.get_phase(phase_name)
        return phase.order if phase else -1
    
    @abstractmethod
    def validate_action(self, action: Action, game_state: Optional[Any] = None) -> ValidationResult:
        """
        Validate an action according to this edition's rules.
        
        Args:
            action: The action to validate.
            game_state: Optional current game state for context.
            
        Returns:
            ValidationResult indicating if the action is valid.
        """
        pass
    
    def is_action_allowed_in_phase(self, action_type: ActionType, phase_name: str) -> bool:
        """Check if an action type is allowed in a given phase."""
        phase = self.get_phase(phase_name)
        if not phase:
            return False
        return action_type in phase.allowed_actions
    
    def get_next_phase(self, current_phase: str) -> Optional[str]:
        """Get the next phase after the current one."""
        current_order = self.get_phase_order(current_phase)
        if current_order < 0:
            return None
        
        for phase in self.phases:
            if phase.order == current_order + 1:
                return phase.name
        return None
    
    def __str__(self) -> str:
        return f"{self.edition_name} ({self.edition_code})"


class EditionRegistry:
    """
    Registry for edition plugins.
    
    Provides discovery and access to installed edition plugins.
    
    Example:
        registry = EditionRegistry()
        registry.register(TenthEditionPlugin())
        
        edition = registry.get("10th")
    """
    
    def __init__(self) -> None:
        self._editions: dict[str, EditionPlugin] = {}
        self._default: Optional[str] = None
    
    def register(self, plugin: EditionPlugin, set_default: bool = False) -> None:
        """Register an edition plugin."""
        self._editions[plugin.edition_code] = plugin
        if set_default or self._default is None:
            self._default = plugin.edition_code
    
    def get(self, edition_code: str) -> Optional[EditionPlugin]:
        """Get an edition plugin by code."""
        return self._editions.get(edition_code)
    
    def get_default(self) -> Optional[EditionPlugin]:
        """Get the default edition plugin."""
        if self._default:
            return self._editions.get(self._default)
        return None
    
    @property
    def available_editions(self) -> list[str]:
        """List available edition codes."""
        return list(self._editions.keys())
    
    def __len__(self) -> int:
        return len(self._editions)
    
    def __contains__(self, edition_code: str) -> bool:
        return edition_code in self._editions


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
