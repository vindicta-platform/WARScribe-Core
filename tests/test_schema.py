"""
Unit tests for WARScribe-Core schema.
"""

import json
import pytest
from uuid import uuid4

from warscribe.schema.unit import UnitReference
from warscribe.schema.action import (
    ActionType,
    MoveAction,
    ShootAction,
    ChargeAction,
    FightAction,
)
from warscribe.schema.transcript import GameTranscript, Player


class TestUnitReference:
    """Tests for UnitReference model."""

    def test_unit_reference_creation(self):
        """UnitReference should be creatable."""
        unit = UnitReference(name="Intercessors A", faction="Space Marines")
        
        assert unit.name == "Intercessors A"
        assert unit.faction == "Space Marines"

    def test_unit_reference_str(self):
        """str() should return readable format."""
        unit = UnitReference(name="Crisis Suits", faction="T'au Empire")
        
        assert "Crisis Suits" in str(unit)
        assert "T'au Empire" in str(unit)

    def test_short_ref(self):
        """short_ref should truncate long names."""
        unit = UnitReference(name="Very Long Unit Name Here", faction="F")
        
        short = unit.short_ref()
        assert len(short) <= 12


class TestActions:
    """Tests for Action models."""

    def test_move_action(self):
        """MoveAction should record movement."""
        actor = UnitReference(name="Squad A", faction="Marines")
        
        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.0
        )
        
        assert action.action_type == ActionType.MOVE
        assert action.distance_inches == 6.0

    def test_shoot_action(self):
        """ShootAction should record shooting."""
        actor = UnitReference(name="Devastators", faction="Marines")
        target = UnitReference(name="Orks", faction="Orks")
        
        action = ShootAction(
            turn=2,
            phase="shooting",
            actor=actor,
            target=target,
            weapon_name="Lascannon",
            shots=2,
            hits=1,
            wounds=1,
            damage_dealt=6
        )
        
        assert action.action_type == ActionType.SHOOT
        assert action.damage_dealt == 6

    def test_charge_action(self):
        """ChargeAction should record charges."""
        actor = UnitReference(name="Assault Marines", faction="Marines")
        target = UnitReference(name="Guardsmen", faction="Astra Militarum")
        
        action = ChargeAction(
            turn=2,
            phase="charge",
            actor=actor,
            targets=[target],
            charge_roll=(4, 5),
            distance_needed=7.0,
            made_charge=True
        )
        
        assert action.action_type == ActionType.CHARGE
        assert action.made_charge

    def test_fight_action(self):
        """FightAction should record melee."""
        actor = UnitReference(name="Assault Marines", faction="Marines")
        target = UnitReference(name="Guardsmen", faction="Astra Militarum")
        
        action = FightAction(
            turn=2,
            phase="fight",
            actor=actor,
            target=target,
            weapon_name="Chainsword",
            attacks=10,
            hits=7,
            wounds=5,
            models_killed=5
        )
        
        assert action.action_type == ActionType.FIGHT
        assert action.models_killed == 5


class TestGameTranscript:
    """Tests for GameTranscript model."""

    def test_transcript_creation(self):
        """GameTranscript should be creatable."""
        p1 = Player(name="Alice", faction="Space Marines")
        p2 = Player(name="Bob", faction="Orks")
        
        transcript = GameTranscript(
            player1=p1,
            player2=p2,
            mission="Scorched Earth"
        )
        
        assert transcript.player1.name == "Alice"
        assert transcript.mission == "Scorched Earth"

    def test_add_action(self):
        """add_action should append to actions list."""
        p1 = Player(name="A", faction="F1")
        p2 = Player(name="B", faction="F2")
        transcript = GameTranscript(player1=p1, player2=p2)
        
        actor = UnitReference(name="Unit", faction="F1")
        action = MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6)
        
        transcript.add_action(action)
        
        assert len(transcript.actions) == 1

    def test_get_actions_for_turn(self):
        """get_actions_for_turn should filter by turn."""
        p1 = Player(name="A", faction="F1")
        p2 = Player(name="B", faction="F2")
        transcript = GameTranscript(player1=p1, player2=p2)
        
        actor = UnitReference(name="Unit", faction="F1")
        
        transcript.add_action(MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6))
        transcript.add_action(MoveAction(turn=2, phase="movement", actor=actor, distance_inches=6))
        transcript.add_action(MoveAction(turn=2, phase="movement", actor=actor, distance_inches=6))
        
        turn2_actions = transcript.get_actions_for_turn(2)
        
        assert len(turn2_actions) == 2

    def test_json_serialization(self):
        """Transcript should round-trip through JSON."""
        p1 = Player(name="Alice", faction="Space Marines")
        p2 = Player(name="Bob", faction="Orks")
        
        transcript = GameTranscript(
            player1=p1,
            player2=p2,
            mission="Test Mission"
        )
        
        actor = UnitReference(name="Unit", faction="F1")
        transcript.add_action(MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6))
        
        # Serialize
        json_str = transcript.to_json()
        
        # Deserialize
        restored = GameTranscript.from_json(json_str)
        
        assert restored.player1.name == "Alice"
        assert restored.mission == "Test Mission"
        assert len(restored.actions) == 1
