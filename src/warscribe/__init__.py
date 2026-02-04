"""
WARScribe-Core: The notation engine for Warhammer gameplay.

Edition-agnostic action notation for recording games.
"""

from warscribe.schema.action import (
    Action,
    ActionType,
    ChargeAction,
    FightAction,
    MoveAction,
    ShootAction,
)
from warscribe.schema.transcript import GameTranscript
from warscribe.schema.unit import UnitReference

__version__ = "0.1.0"

__all__ = [
    "Action",
    "ActionType",
    "ChargeAction",
    "FightAction",
    "GameTranscript",
    "MoveAction",
    "ShootAction",
    "UnitReference",
]
