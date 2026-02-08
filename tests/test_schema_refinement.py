"""Tests for schema refinement (Week 1 tasks)."""

from warscribe.schema.action import ShootAction, FightAction
from warscribe.schema.unit import UnitReference
from warscribe.edition import GamePhase


def test_shoot_action_refinement():
    unit = UnitReference(name="Space Marine", faction="Imperium")
    target = UnitReference(name="Ork Boy", faction="Orks")

    action = ShootAction(
        turn=1,
        phase=GamePhase.SHOOTING,
        actor=unit,
        target=target,
        weapon_name="Bolt Rifle",
        weapon_profile={"S": "4", "AP": "-1", "D": "1"},
        shots=2,
        modifiers=["heavy"],
        dice_rolls={"hit": [4, 6], "wound": [3, 5], "save": [2]},
        hits=2,
        wounds=2,
        saves_failed=1,
        damage_dealt=1,
        models_killed=0,
    )

    assert action.weapon_profile["S"] == "4"
    assert "heavy" in action.modifiers
    assert action.dice_rolls["hit"] == [4, 6]


def test_fight_action_refinement():
    unit = UnitReference(name="Intercessor", faction="Imperium")
    target = UnitReference(name="Gretchin", faction="Orks")

    action = FightAction(
        turn=1,
        phase=GamePhase.FIGHT,
        actor=unit,
        target=target,
        weapon_name="Astartes Chainsword",
        weapon_profile={"S": "4", "AP": "-1", "D": "1"},
        attacks=3,
        modifiers=["sustained hits 1"],
        dice_rolls={"hit": [4, 5, 2], "wound": [4, 6]},
        hits=2,
        wounds=2,
    )

    assert action.weapon_profile["AP"] == "-1"
    assert "sustained hits 1" in action.modifiers
    assert len(action.dice_rolls["hit"]) == 3
