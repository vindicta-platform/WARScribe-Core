"""
Unit tests for WARScribe-Core schema.
"""

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

        action = MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6.0)

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
            damage_dealt=6,
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
            made_charge=True,
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
            models_killed=5,
        )

        assert action.action_type == ActionType.FIGHT
        assert action.models_killed == 5


class TestGameTranscript:
    """Tests for GameTranscript model."""

    def test_transcript_creation(self):
        """GameTranscript should be creatable."""
        p1 = Player(name="Alice", faction="Space Marines")
        p2 = Player(name="Bob", faction="Orks")

        transcript = GameTranscript(player1=p1, player2=p2, mission="Scorched Earth")

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

        transcript.add_action(
            MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6)
        )
        transcript.add_action(
            MoveAction(turn=2, phase="movement", actor=actor, distance_inches=6)
        )
        transcript.add_action(
            MoveAction(turn=2, phase="movement", actor=actor, distance_inches=6)
        )

        turn2_actions = transcript.get_actions_for_turn(2)

        assert len(turn2_actions) == 2

    def test_json_serialization(self):
        """Transcript should round-trip through JSON."""
        p1 = Player(name="Alice", faction="Space Marines")
        p2 = Player(name="Bob", faction="Orks")

        transcript = GameTranscript(player1=p1, player2=p2, mission="Test Mission")

        actor = UnitReference(name="Unit", faction="F1")
        transcript.add_action(
            MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6)
        )

        # Serialize
        json_str = transcript.to_json()

        # Deserialize
        restored = GameTranscript.from_json(json_str)

        assert restored.player1.name == "Alice"
        assert restored.mission == "Test Mission"
        assert len(restored.actions) == 1


class TestActionRoundTripSerialization:
    """Tests for action round-trip serialization through JSON."""

    def test_move_action_roundtrip(self):
        """MoveAction should serialize and deserialize correctly."""
        actor = UnitReference(name="Intercessors", faction="Space Marines")
        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.5,
            is_advance=True,
            terrain_crossed=["ruins", "crater"],
        )

        json_str = action.model_dump_json()
        restored = MoveAction.model_validate_json(json_str)

        assert restored.action_type == ActionType.MOVE
        assert restored.distance_inches == 6.5
        assert restored.is_advance is True
        assert "ruins" in restored.terrain_crossed

    def test_shoot_action_roundtrip(self):
        """ShootAction should preserve all dice results."""
        actor = UnitReference(name="Devastators", faction="Marines")
        target = UnitReference(name="Boyz", faction="Orks")

        action = ShootAction(
            turn=2,
            phase="shooting",
            actor=actor,
            target=target,
            weapon_name="Multi-melta",
            shots=4,
            hits=3,
            wounds=2,
            saves_failed=2,
            damage_dealt=12,
            models_killed=2,
        )

        json_str = action.model_dump_json()
        restored = ShootAction.model_validate_json(json_str)

        assert restored.weapon_name == "Multi-melta"
        assert restored.damage_dealt == 12
        assert restored.models_killed == 2

    def test_charge_action_roundtrip(self):
        """ChargeAction should preserve roll and targets."""
        actor = UnitReference(name="Assault Marines", faction="Marines")
        target1 = UnitReference(name="Guardsmen A", faction="Astra Militarum")
        target2 = UnitReference(name="Guardsmen B", faction="Astra Militarum")

        action = ChargeAction(
            turn=2,
            phase="charge",
            actor=actor,
            targets=[target1, target2],
            charge_roll=(5, 6),
            distance_needed=8.0,
            made_charge=True,
        )

        json_str = action.model_dump_json()
        restored = ChargeAction.model_validate_json(json_str)

        assert len(restored.targets) == 2
        assert restored.charge_roll == (5, 6)
        assert restored.made_charge is True

    def test_fight_action_roundtrip(self):
        """FightAction should preserve combat results."""
        actor = UnitReference(name="Terminators", faction="Marines")
        target = UnitReference(name="Genestealers", faction="Tyranids")

        action = FightAction(
            turn=3,
            phase="fight",
            actor=actor,
            target=target,
            weapon_name="Thunder Hammer",
            attacks=5,
            hits=3,
            wounds=3,
            saves_failed=2,
            damage_dealt=6,
            models_killed=2,
        )

        json_str = action.model_dump_json()
        restored = FightAction.model_validate_json(json_str)

        assert restored.weapon_name == "Thunder Hammer"
        assert restored.damage_dealt == 6


class TestEdgeCases:
    """Tests for edge cases and validation boundaries."""

    def test_move_zero_distance(self):
        """Movement of 0 inches should be valid."""
        actor = UnitReference(name="Unit", faction="F1")
        action = MoveAction(turn=1, phase="movement", actor=actor, distance_inches=0.0)

        assert action.distance_inches == 0.0

    def test_move_fractional_distance(self):
        """Fractional movement should be preserved."""
        actor = UnitReference(name="Unit", faction="F1")
        action = MoveAction(
            turn=1, phase="movement", actor=actor, distance_inches=6.283
        )

        assert action.distance_inches == 6.283

    def test_shoot_zero_hits(self):
        """Shooting with zero hits is valid (all misses)."""
        actor = UnitReference(name="Shooter", faction="F1")
        target = UnitReference(name="Target", faction="F2")

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
        assert action.damage_dealt == 0

    def test_charge_failed(self):
        """Failed charge should be recordable."""
        actor = UnitReference(name="Unit", faction="F1")
        target = UnitReference(name="Target", faction="F2")

        action = ChargeAction(
            turn=2,
            phase="charge",
            actor=actor,
            targets=[target],
            charge_roll=(1, 2),
            distance_needed=10.0,
            made_charge=False,
        )

        assert action.made_charge is False
        assert sum(action.charge_roll) < action.distance_needed

    def test_unit_reference_with_special_characters(self):
        """Unit names with special characters should work."""
        unit = UnitReference(name="T'au Commander (Crisis)", faction="T'au Empire")

        assert "T'au" in unit.name
        assert "(Crisis)" in unit.name

    def test_action_with_notes(self):
        """Actions can include notes."""
        actor = UnitReference(name="Unit", faction="F1")
        action = MoveAction(
            turn=1,
            phase="movement",
            actor=actor,
            distance_inches=6.0,
            notes='Moved through difficult terrain, -2" penalty applied',
        )

        assert "difficult terrain" in action.notes

    def test_transcript_empty_actions(self):
        """Transcript with no actions should serialize correctly."""
        p1 = Player(name="A", faction="F1")
        p2 = Player(name="B", faction="F2")
        transcript = GameTranscript(player1=p1, player2=p2)

        json_str = transcript.to_json()
        restored = GameTranscript.from_json(json_str)

        assert len(restored.actions) == 0

    def test_transcript_multiple_action_types(self):
        """Transcript should handle mixed action types."""
        p1 = Player(name="A", faction="F1")
        p2 = Player(name="B", faction="F2")
        transcript = GameTranscript(player1=p1, player2=p2)

        actor = UnitReference(name="Unit A", faction="F1")
        target = UnitReference(name="Target B", faction="F2")

        transcript.add_action(
            MoveAction(turn=1, phase="movement", actor=actor, distance_inches=6)
        )
        transcript.add_action(
            ShootAction(
                turn=1,
                phase="shooting",
                actor=actor,
                target=target,
                weapon_name="Bolter",
                shots=2,
                hits=1,
                wounds=1,
                damage_dealt=1,
            )
        )
        transcript.add_action(
            ChargeAction(
                turn=1,
                phase="charge",
                actor=actor,
                targets=[target],
                charge_roll=(4, 4),
                distance_needed=7,
                made_charge=True,
            )
        )
        transcript.add_action(
            FightAction(
                turn=1,
                phase="fight",
                actor=actor,
                target=target,
                weapon_name="Chainsword",
                attacks=3,
                hits=2,
                wounds=1,
                models_killed=1,
            )
        )

        assert len(transcript.actions) == 4

        # Verify each type is correct
        types = [a.action_type for a in transcript.actions]
        assert ActionType.MOVE in types
        assert ActionType.SHOOT in types
        assert ActionType.CHARGE in types
        assert ActionType.FIGHT in types


class TestActionTypeEnum:
    """Tests for ActionType enum coverage."""

    def test_all_core_action_types_defined(self):
        """Core action types should be defined."""
        assert ActionType.MOVE.value == "move"
        assert ActionType.SHOOT.value == "shoot"
        assert ActionType.CHARGE.value == "charge"
        assert ActionType.FIGHT.value == "fight"

    def test_additional_action_types_defined(self):
        """Additional action types should be defined for future use."""
        assert ActionType.ADVANCE.value == "advance"
        assert ActionType.FALL_BACK.value == "fall_back"
        assert ActionType.CONSOLIDATE.value == "consolidate"
        assert ActionType.PILE_IN.value == "pile_in"
        assert ActionType.HEROIC_INTERVENTION.value == "heroic_intervention"
        assert ActionType.STRATAGEM.value == "stratagem"
        assert ActionType.ABILITY.value == "ability"
        assert ActionType.OBJECTIVE.value == "objective"
