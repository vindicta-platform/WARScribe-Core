"""
10th Edition Plugin for WARScribe-Core.

Implements Warhammer 40,000 10th Edition rules.
"""

from typing import Any, Optional, Sequence

from warscribe.edition.plugin import (
    EditionPlugin,
    GamePhase,
    PhaseDefinition,
    ValidationResult,
)
from warscribe.schema.action import (
    Action,
    ActionType,
    MoveAction,
    ChargeAction,
    ShootAction,
    FightAction,
)


class TenthEditionPlugin(EditionPlugin):
    """
    Warhammer 40,000 10th Edition rules implementation.
    
    10th Edition key features:
    - Simplified phase structure
    - No more Psychic phase (integrated into other phases)
    - Command Phase for abilities and stratagems
    """
    
    @property
    def edition_name(self) -> str:
        return "Warhammer 40,000 10th Edition"
    
    @property
    def edition_code(self) -> str:
        return "10th"
    
    @property
    def phases(self) -> Sequence[PhaseDefinition]:
        """
        10th Edition phases.
        
        Note: No separate Psychic phase in 10th Edition.
        """
        return [
            PhaseDefinition(
                name=GamePhase.COMMAND,
                display_name="Command Phase",
                order=0,
                allowed_actions=[ActionType.STRATAGEM, ActionType.ABILITY],
                description="Use abilities and generate Command Points.",
            ),
            PhaseDefinition(
                name=GamePhase.MOVEMENT,
                display_name="Movement Phase",
                order=1,
                allowed_actions=[
                    ActionType.MOVE,
                    ActionType.ADVANCE,
                    ActionType.FALL_BACK,
                ],
                description="Move your units across the battlefield.",
            ),
            PhaseDefinition(
                name=GamePhase.SHOOTING,
                display_name="Shooting Phase",
                order=2,
                allowed_actions=[ActionType.SHOOT, ActionType.STRATAGEM],
                description="Shoot with ranged weapons.",
            ),
            PhaseDefinition(
                name=GamePhase.CHARGE,
                display_name="Charge Phase",
                order=3,
                allowed_actions=[
                    ActionType.CHARGE,
                    ActionType.HEROIC_INTERVENTION,
                    ActionType.STRATAGEM,
                ],
                description="Charge into close combat.",
            ),
            PhaseDefinition(
                name=GamePhase.FIGHT,
                display_name="Fight Phase",
                order=4,
                allowed_actions=[
                    ActionType.FIGHT,
                    ActionType.PILE_IN,
                    ActionType.CONSOLIDATE,
                    ActionType.STRATAGEM,
                ],
                description="Fight in close combat.",
            ),
            PhaseDefinition(
                name=GamePhase.MORALE,
                display_name="Morale Phase",
                order=5,
                allowed_actions=[ActionType.ABILITY],
                description="Test unit morale.",
                is_optional=True,
            ),
        ]
    
    def validate_action(
        self, action: Action, game_state: Optional[Any] = None
    ) -> ValidationResult:
        """
        Validate an action against 10th Edition rules.
        
        Checks:
        - Action type allowed in current phase
        - Movement within limits
        - Charge distance calculations
        """
        result = ValidationResult.success()
        
        # Check phase allows action type
        if not self.is_action_allowed_in_phase(action.action_type, action.phase):
            return ValidationResult.failure(
                f"Action type '{action.action_type.value}' not allowed in "
                f"'{action.phase}' phase."
            )
        
        # Type-specific validation
        if isinstance(action, MoveAction):
            result = self._validate_move(action, result)
        elif isinstance(action, ChargeAction):
            result = self._validate_charge(action, result)
        elif isinstance(action, ShootAction):
            result = self._validate_shoot(action, result)
        elif isinstance(action, FightAction):
            result = self._validate_fight(action, result)
        
        return result
    
    def _validate_move(
        self, action: MoveAction, result: ValidationResult
    ) -> ValidationResult:
        """Validate a move action."""
        # Basic movement distance check
        if action.distance_inches < 0:
            return ValidationResult.failure("Movement distance cannot be negative.")
        
        # Warn on excessive movement
        if action.distance_inches > 24:
            result.add_warning(
                f"Movement of {action.distance_inches}\" is unusually high."
            )
        
        # Check advance flag consistency
        if action.is_advance and action.is_fall_back:
            return ValidationResult.failure(
                "A unit cannot both Advance and Fall Back in the same move."
            )
        
        return result
    
    def _validate_charge(
        self, action: ChargeAction, result: ValidationResult
    ) -> ValidationResult:
        """Validate a charge action."""
        # Charge roll must be 2D6
        if len(action.charge_roll) != 2:
            return ValidationResult.failure("Charge roll must be 2D6.")
        
        d1, d2 = action.charge_roll
        if not (1 <= d1 <= 6 and 1 <= d2 <= 6):
            return ValidationResult.failure("Dice values must be between 1 and 6.")
        
        # Calculate total charge distance
        total_roll = d1 + d2
        
        # Check if charge was made correctly
        if action.made_charge:
            if total_roll < action.distance_needed:
                result.add_warning(
                    f"Charge marked as successful but roll ({total_roll}) "
                    f"is less than distance needed ({action.distance_needed})."
                )
        
        return result
    
    def _validate_shoot(
        self, action: ShootAction, result: ValidationResult
    ) -> ValidationResult:
        """Validate a shooting action.
        
        Issue #6: Action validation working.
        """
        # Basic sanity checks
        if action.shots < 1:
            return ValidationResult.failure("Must have at least 1 shot.")
        
        # Hits cannot exceed shots
        if action.hits > action.shots:
            return ValidationResult.failure(
                f"Hits ({action.hits}) cannot exceed shots ({action.shots})."
            )
        
        # Wounds cannot exceed hits
        if action.wounds > action.hits:
            result.add_warning(
                f"Wounds ({action.wounds}) exceed hits ({action.hits}). "
                "Verify re-rolls or abilities."
            )
        
        # Saves failed cannot exceed wounds
        if action.saves_failed > action.wounds:
            result.add_warning(
                f"Saves failed ({action.saves_failed}) exceed wounds ({action.wounds})."
            )
        
        # Models killed should be reasonable
        if action.models_killed > action.saves_failed:
            result.add_warning(
                f"Models killed ({action.models_killed}) exceeds saves failed "
                f"({action.saves_failed}). Multi-damage weapon?"
            )
        
        return result
    
    def _validate_fight(
        self, action: FightAction, result: ValidationResult
    ) -> ValidationResult:
        """Validate a fight (melee) action.
        
        Issue #6: Action validation working.
        """
        # Basic sanity checks
        if action.attacks < 1:
            return ValidationResult.failure("Must have at least 1 attack.")
        
        # Hits cannot exceed attacks
        if action.hits > action.attacks:
            return ValidationResult.failure(
                f"Hits ({action.hits}) cannot exceed attacks ({action.attacks})."
            )
        
        # Same cascade validation as shooting
        if action.wounds > action.hits:
            result.add_warning(
                f"Wounds ({action.wounds}) exceed hits ({action.hits}). "
                "Verify re-rolls or abilities."
            )
        
        if action.saves_failed > action.wounds:
            result.add_warning(
                f"Saves failed ({action.saves_failed}) exceed wounds ({action.wounds})."
            )
        
        return result


# Register plugin when module is imported
def _register() -> None:
    """Register the 10th Edition plugin."""
    from warscribe.edition import register_edition
    register_edition(TenthEditionPlugin(), set_default=True)

_register()
