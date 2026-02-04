"""Tests for edition abstraction layer."""

import pytest

from warscribe.edition import (
    EditionPlugin,
    EditionRegistry,
    GamePhase,
    PhaseDefinition,
    ValidationResult,
    get_edition_registry,
    register_edition,
)
from warscribe.edition.tenth import TenthEditionPlugin
from warscribe.schema.action import ActionType, MoveAction, ChargeAction
from warscribe.schema.unit import UnitReference


class TestPhaseDefinition:
    """Tests for PhaseDefinition."""
    
    def test_create_phase(self):
        phase = PhaseDefinition(
            name="movement",
            display_name="Movement Phase",
            order=1,
            allowed_actions=[ActionType.MOVE],
        )
        assert phase.name == "movement"
        assert phase.order == 1
        assert ActionType.MOVE in phase.allowed_actions


class TestValidationResult:
    """Tests for ValidationResult."""
    
    def test_success(self):
        result = ValidationResult.success()
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_failure(self):
        result = ValidationResult.failure("Error 1", "Error 2")
        assert not result.is_valid
        assert len(result.errors) == 2
    
    def test_add_warning(self):
        result = ValidationResult.success()
        result.add_warning("Warning 1")
        assert result.is_valid  # Still valid
        assert len(result.warnings) == 1


class TestEditionRegistry:
    """Tests for EditionRegistry."""
    
    def test_register_and_get(self):
        registry = EditionRegistry()
        plugin = TenthEditionPlugin()
        registry.register(plugin)
        
        assert "10th" in registry
        assert registry.get("10th") is plugin
    
    def test_default_edition(self):
        registry = EditionRegistry()
        plugin = TenthEditionPlugin()
        registry.register(plugin, set_default=True)
        
        assert registry.get_default() is plugin
    
    def test_available_editions(self):
        registry = EditionRegistry()
        registry.register(TenthEditionPlugin())
        
        assert "10th" in registry.available_editions


class TestTenthEditionPlugin:
    """Tests for 10th Edition plugin."""
    
    @pytest.fixture
    def plugin(self):
        return TenthEditionPlugin()
    
    @pytest.fixture
    def unit_ref(self):
        return UnitReference(name="Space Marines", faction="Imperium")
    
    def test_edition_info(self, plugin):
        assert plugin.edition_code == "10th"
        assert "10th Edition" in plugin.edition_name
    
    def test_phases_defined(self, plugin):
        phases = plugin.phases
        assert len(phases) >= 5  # At least: Command, Movement, Shooting, Charge, Fight
        
        # Check no psychic phase (10th edition feature)
        phase_names = [p.name for p in phases]
        assert GamePhase.PSYCHIC not in phase_names
    
    def test_phase_order(self, plugin):
        # Movement should come after Command
        assert plugin.get_phase_order(GamePhase.COMMAND) < plugin.get_phase_order(GamePhase.MOVEMENT)
    
    def test_get_next_phase(self, plugin):
        next_phase = plugin.get_next_phase(GamePhase.MOVEMENT)
        assert next_phase == GamePhase.SHOOTING
    
    def test_action_allowed_in_phase(self, plugin):
        assert plugin.is_action_allowed_in_phase(ActionType.MOVE, GamePhase.MOVEMENT)
        assert not plugin.is_action_allowed_in_phase(ActionType.MOVE, GamePhase.SHOOTING)
    
    def test_validate_move_action(self, plugin, unit_ref):
        action = MoveAction(
            turn=1,
            phase=GamePhase.MOVEMENT,
            actor=unit_ref,
            distance_inches=6.0,
        )
        result = plugin.validate_action(action)
        assert result.is_valid
    
    def test_validate_move_wrong_phase(self, plugin, unit_ref):
        action = MoveAction(
            turn=1,
            phase=GamePhase.SHOOTING,  # Wrong phase!
            actor=unit_ref,
            distance_inches=6.0,
        )
        result = plugin.validate_action(action)
        assert not result.is_valid
        assert "not allowed" in result.errors[0].lower()
    
    def test_validate_charge_roll(self, plugin, unit_ref):
        target = UnitReference(name="Orks", faction="Orks")
        action = ChargeAction(
            turn=1,
            phase=GamePhase.CHARGE,
            actor=unit_ref,
            targets=[target],
            charge_roll=(4, 5),
            distance_needed=8.0,
            made_charge=True,
        )
        result = plugin.validate_action(action)
        assert result.is_valid
    
    def test_validate_impossible_charge(self, plugin, unit_ref):
        target = UnitReference(name="Orks", faction="Orks")
        action = ChargeAction(
            turn=1,
            phase=GamePhase.CHARGE,
            actor=unit_ref,
            targets=[target],
            charge_roll=(2, 3),  # Total 5
            distance_needed=8.0,  # Need 8!
            made_charge=True,  # Marked as success but shouldn't be
        )
        result = plugin.validate_action(action)
        assert result.is_valid  # Still valid but should have warning
        assert len(result.warnings) > 0
