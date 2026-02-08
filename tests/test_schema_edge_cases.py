"""
Additional unit tests for WARScribe-Core schema.

Extends test coverage for Issue #5:
- Edge case coverage
- Round-trip serialization tests
- All action types tested
"""

import pytest
from uuid import uuid4
from pydantic import ValidationError

from warscribe.schema.unit import UnitReference
from warscribe.schema.action import (
    ActionResult,
    MoveAction,
    ShootAction,
    ChargeAction,
    RelativeDistance,
)
from warscribe.schema.transcript import GameTranscript, Player


class TestActionEdgeCases:
    """Edge case tests for Action models."""

    def test_move_action_zero_distance(self):
        """MoveAction should allow 0 distance (stationary)."""
        actor = UnitReference(name="Squad A", faction="Marines")

        action = MoveAction(turn=1, phase="movement", actor=actor, distance_inches=0.0)

        assert action.distance_inches == 0.0

    def test_move_action_rejects_negative_distance(self):
        """MoveAction should reject negative distance."""
        actor = UnitReference(name="Squad A", faction="Marines")

        with pytest.raises(ValidationError):
            MoveAction(turn=1, phase="movement", actor=actor, distance_inches=-1.0)

    def test_move_action_with_relative_distances(self):
        """MoveAction should track relative distances."""
        actor = UnitReference(name="Squad A", faction="Marines")
        target_id = uuid4()

        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.0,
            relative_distances=[
                RelativeDistance(
                    target_unit_id=target_id,
                    target_unit_name="Enemy Squad",
                    delta_inches=-4.0,  # Moved 4" closer
                    final_distance=8.0,
                )
            ],
        )

        assert len(action.relative_distances) == 1
        assert action.relative_distances[0].delta_inches == -4.0

    def test_shoot_action_zero_hits(self):
        """ShootAction should allow 0 hits (all missed)."""
        actor = UnitReference(name="Squad A", faction="Marines")
        target = UnitReference(name="Orks", faction="Orks")

        action = ShootAction(
            turn=1,
            phase="shooting",
            actor=actor,
            target=target,
            weapon_name="Bolter",
            shots=10,
            hits=0,
            wounds=0,
            damage_dealt=0,
        )

        assert action.hits == 0
        assert action.wounds == 0

    def test_charge_action_failed_charge(self):
        """ChargeAction should record failed charges."""
        actor = UnitReference(name="Assault Marines", faction="Marines")
        target = UnitReference(name="Guardsmen", faction="Astra Militarum")

        action = ChargeAction(
            turn=2,
            phase="charge",
            actor=actor,
            targets=[target],
            charge_roll=(2, 3),  # Total 5
            distance_needed=9.0,
            made_charge=False,
        )

        assert not action.made_charge
        assert sum(action.charge_roll) < action.distance_needed

    def test_charge_action_multiple_targets(self):
        """ChargeAction should support multiple targets."""
        actor = UnitReference(name="Assault Marines", faction="Marines")
        target1 = UnitReference(name="Guardsmen A", faction="Astra Militarum")
        target2 = UnitReference(name="Guardsmen B", faction="Astra Militarum")

        action = ChargeAction(
            turn=2,
            phase="charge",
            actor=actor,
            targets=[target1, target2],
            charge_roll=(5, 6),
            distance_needed=7.0,
            made_charge=True,
        )

        assert len(action.targets) == 2

    def test_action_result_states(self):
        """All ActionResult states should be valid."""
        actor = UnitReference(name="Squad A", faction="Marines")

        for result_state in ActionResult:
            action = MoveAction(
                turn=1,
                phase="movement",
                actor=actor,
                distance_inches=6.0,
                result=result_state,
            )
            assert action.result == result_state

    def test_action_with_notes(self):
        """Actions should support optional notes."""
        actor = UnitReference(name="Squad A", faction="Marines")

        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.0,
            notes="Moved through difficult terrain",
        )

        assert action.notes == "Moved through difficult terrain"


class TestMoveActionModifiers:
    """Tests for MoveAction with modifiers (advance, fall back)."""

    def test_advance_action(self):
        """MoveAction with is_advance=True."""
        actor = UnitReference(name="Squad A", faction="Marines")

        action = MoveAction(
            turn=1, phase="movement", actor=actor, distance_inches=12.0, is_advance=True
        )

        assert action.is_advance
        assert not action.is_fall_back

    def test_fall_back_action(self):
        """MoveAction with is_fall_back=True."""
        actor = UnitReference(name="Squad A", faction="Marines")

        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.0,
            is_fall_back=True,
        )

        assert action.is_fall_back
        assert not action.is_advance

    def test_terrain_crossed(self):
        """MoveAction should track terrain crossed."""
        actor = UnitReference(name="Squad A", faction="Marines")

        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.0,
            terrain_crossed=["Ruins", "Crater"],
        )

        assert "Ruins" in action.terrain_crossed
        assert len(action.terrain_crossed) == 2


class TestRoundTripSerialization:
    """Tests for JSON round-trip serialization."""

    def test_move_action_round_trip(self):
        """MoveAction should serialize and deserialize correctly."""
        actor = UnitReference(name="Squad A", faction="Marines")

        original = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.5,
            is_advance=True,
            terrain_crossed=["Ruins"],
        )

        json_str = original.model_dump_json()
        restored = MoveAction.model_validate_json(json_str)

        assert restored.distance_inches == original.distance_inches
        assert restored.is_advance == original.is_advance
        assert restored.terrain_crossed == original.terrain_crossed

    def test_shoot_action_round_trip(self):
        """ShootAction should serialize and deserialize correctly."""
        actor = UnitReference(name="Squad A", faction="Marines")
        target = UnitReference(name="Orks", faction="Orks")

        original = ShootAction(
            turn=2,
            phase="shooting",
            actor=actor,
            target=target,
            weapon_name="Lascannon",
            shots=2,
            hits=1,
            wounds=1,
            damage_dealt=6,
            models_killed=1,
        )

        json_str = original.model_dump_json()
        restored = ShootAction.model_validate_json(json_str)

        assert restored.weapon_name == original.weapon_name
        assert restored.damage_dealt == original.damage_dealt
        assert restored.target.name == original.target.name

    def test_charge_action_round_trip(self):
        """ChargeAction should serialize and deserialize correctly."""
        actor = UnitReference(name="Assault Marines", faction="Marines")
        target = UnitReference(name="Guardsmen", faction="Astra Militarum")

        original = ChargeAction(
            turn=2,
            phase="charge",
            actor=actor,
            targets=[target],
            charge_roll=(4, 5),
            distance_needed=7.0,
            made_charge=True,
        )

        json_str = original.model_dump_json()
        restored = ChargeAction.model_validate_json(json_str)

        assert restored.made_charge == original.made_charge
        assert restored.charge_roll == original.charge_roll

    def test_complex_transcript_round_trip(self):
        """Complex GameTranscript with multiple actions should round-trip."""
        p1 = Player(name="Alice", faction="Space Marines")
        p2 = Player(name="Bob", faction="Orks")

        transcript = GameTranscript(player1=p1, player2=p2, mission="Scorched Earth")

        # Add various actions
        actor1 = UnitReference(name="Intercessors", faction="Space Marines")
        actor2 = UnitReference(name="Devastators", faction="Space Marines")
        target = UnitReference(name="Boyz", faction="Orks")

        transcript.add_action(
            MoveAction(turn=1, phase="movement", actor=actor1, distance_inches=6.0)
        )
        transcript.add_action(
            ShootAction(
                turn=1,
                phase="shooting",
                actor=actor2,
                target=target,
                weapon_name="Lascannon",
                shots=2,
                hits=1,
                wounds=1,
                damage_dealt=6,
            )
        )

        json_str = transcript.to_json()
        restored = GameTranscript.from_json(json_str)

        assert len(restored.actions) == 2
        assert restored.mission == "Scorched Earth"
