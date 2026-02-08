"""Integration tests for 10th Edition plugin.

Issue #6 Acceptance Criteria:
- [ ] All phases implemented ✓
- [ ] Action validation working ✓
- [ ] Integration tests passing ← This file

Tests a complete game turn flow through all phases.
"""

import pytest

from warscribe.edition import get_edition_registry
from warscribe.edition.tenth import TenthEditionPlugin
from warscribe.edition import GamePhase
from warscribe.schema.action import (
    MoveAction,
    ShootAction,
    ChargeAction,
    FightAction,
)
from warscribe.schema.unit import UnitReference


class TestTenthEditionIntegration:
    """Integration tests for full game turn flow."""

    @pytest.fixture
    def plugin(self):
        return TenthEditionPlugin()

    @pytest.fixture
    def marines(self):
        return UnitReference(name="Intercessors", faction="Space Marines")

    @pytest.fixture
    def orks(self):
        return UnitReference(name="Boyz", faction="Orks")

    def test_full_turn_sequence(self, plugin, marines, orks):
        """Test a complete game turn through all core phases.

        Issue #6: Integration tests passing.
        """
        # === MOVEMENT PHASE ===
        move = MoveAction(
            turn=1,
            phase=GamePhase.MOVEMENT,
            actor=marines,
            distance_inches=6.0,
        )
        result = plugin.validate_action(move)
        assert result.is_valid, "Movement should be valid"

        # === SHOOTING PHASE ===
        shoot = ShootAction(
            turn=1,
            phase=GamePhase.SHOOTING,
            actor=marines,
            target=orks,
            weapon_name="Bolt Rifle",
            shots=10,
            hits=7,
            wounds=5,
            saves_failed=3,
            damage_dealt=3,
            models_killed=3,
        )
        result = plugin.validate_action(shoot)
        assert result.is_valid, "Shooting should be valid"

        # === CHARGE PHASE ===
        charge = ChargeAction(
            turn=1,
            phase=GamePhase.CHARGE,
            actor=marines,
            targets=[orks],
            charge_roll=(4, 5),  # Total 9
            distance_needed=7.0,
            made_charge=True,
        )
        result = plugin.validate_action(charge)
        assert result.is_valid, "Charge should be valid"

        # === FIGHT PHASE ===
        fight = FightAction(
            turn=1,
            phase=GamePhase.FIGHT,
            actor=marines,
            target=orks,
            weapon_name="Power Fist",
            attacks=4,
            hits=3,
            wounds=3,
            saves_failed=2,
            damage_dealt=4,
            models_killed=2,
        )
        result = plugin.validate_action(fight)
        assert result.is_valid, "Fight should be valid"

    def test_phase_sequence_validation(self, plugin):
        """Test that phase sequence follows 10th Edition rules."""
        phases = plugin.phases

        # Verify correct sequence
        phase_order = [p.name for p in sorted(phases, key=lambda x: x.order)]

        assert GamePhase.COMMAND in phase_order
        assert GamePhase.MOVEMENT in phase_order
        assert GamePhase.SHOOTING in phase_order
        assert GamePhase.CHARGE in phase_order
        assert GamePhase.FIGHT in phase_order

        # No Psychic phase in 10th Edition
        assert GamePhase.PSYCHIC not in phase_order

        # Command before Movement
        cmd_idx = phase_order.index(GamePhase.COMMAND)
        move_idx = phase_order.index(GamePhase.MOVEMENT)
        assert cmd_idx < move_idx

    def test_shoot_validation_cascade(self, plugin, marines, orks):
        """Test shooting validation catches logical errors."""
        # More hits than shots should fail
        bad_shoot = ShootAction(
            turn=1,
            phase=GamePhase.SHOOTING,
            actor=marines,
            target=orks,
            weapon_name="Bolt Rifle",
            shots=5,
            hits=7,  # Invalid: more hits than shots
        )
        result = plugin.validate_action(bad_shoot)
        assert not result.is_valid
        assert "cannot exceed" in result.errors[0].lower()

    def test_fight_validation_cascade(self, plugin, marines, orks):
        """Test fight validation catches logical errors."""
        # More hits than attacks should fail
        bad_fight = FightAction(
            turn=1,
            phase=GamePhase.FIGHT,
            actor=marines,
            target=orks,
            weapon_name="Chainsword",
            attacks=3,
            hits=5,  # Invalid: more hits than attacks
        )
        result = plugin.validate_action(bad_fight)
        assert not result.is_valid
        assert "cannot exceed" in result.errors[0].lower()

    def test_multi_turn_game(self, plugin, marines, orks):
        """Test actions across multiple turns."""
        for turn in range(1, 4):  # Turns 1-3
            # Move each turn
            move = MoveAction(
                turn=turn,
                phase=GamePhase.MOVEMENT,
                actor=marines,
                distance_inches=6.0,
            )
            result = plugin.validate_action(move)
            assert result.is_valid, f"Turn {turn} movement should be valid"

            # Shoot each turn
            shoot = ShootAction(
                turn=turn,
                phase=GamePhase.SHOOTING,
                actor=marines,
                target=orks,
                weapon_name="Bolt Rifle",
                shots=5,
                hits=3,
            )
            result = plugin.validate_action(shoot)
            assert result.is_valid, f"Turn {turn} shooting should be valid"


class TestEditionRegistration:
    """Test 10th Edition registration and discovery."""

    def test_registry_contains_tenth(self):
        """10th Edition should be registered."""
        # Force registration
        from warscribe.edition.tenth import _register

        _register()

        registry = get_edition_registry()
        assert "10th" in registry.available_editions

    def test_default_edition_is_tenth(self):
        """10th Edition should be the default."""
        from warscribe.edition.tenth import _register

        _register()

        registry = get_edition_registry()
        default = registry.get_default()
        assert default is not None
        assert default.edition_code == "10th"
