"""
Action models for WARScribe notation.

Core action types per ROADMAP v0.1.0:
- Move
- Shoot  
- Charge
- Fight
"""

from datetime import datetime
from enum import Enum, auto
from typing import Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from warscribe.schema.unit import UnitReference


class ActionType(str, Enum):
    """Types of actions that can be recorded."""
    MOVE = "move"
    SHOOT = "shoot"
    CHARGE = "charge"
    FIGHT = "fight"
    ADVANCE = "advance"
    FALL_BACK = "fall_back"
    CONSOLIDATE = "consolidate"
    PILE_IN = "pile_in"
    HEROIC_INTERVENTION = "heroic_intervention"
    STRATAGEM = "stratagem"
    ABILITY = "ability"
    OBJECTIVE = "objective"


class ActionResult(str, Enum):
    """Result of an action."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"


class BaseAction(BaseModel):
    """Base class for all actions."""
    
    id: UUID = Field(default_factory=uuid4)
    action_type: ActionType
    
    # Timing
    turn: int = Field(..., ge=1, description="Turn number")
    phase: str = Field(..., description="Game phase (e.g., 'movement', 'shooting')")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Actor
    actor: UnitReference = Field(..., description="The unit performing the action")
    
    # Result
    result: ActionResult = ActionResult.PENDING
    
    # Notes
    notes: Optional[str] = Field(None, description="Optional notes about the action")


class MoveAction(BaseAction):
    """A movement action."""
    
    action_type: ActionType = ActionType.MOVE
    
    # Movement details
    distance_inches: float = Field(..., ge=0, description="Distance moved in inches")
    start_position: Optional[tuple[float, float]] = None
    end_position: Optional[tuple[float, float]] = None
    
    # Movement modifiers
    is_advance: bool = False
    is_fall_back: bool = False
    terrain_crossed: list[str] = Field(default_factory=list)


class ShootAction(BaseAction):
    """A shooting action."""
    
    action_type: ActionType = ActionType.SHOOT
    
    # Target
    target: UnitReference = Field(..., description="Unit being shot at")
    
    # Weapon info
    weapon_name: str = Field(..., description="Weapon used")
    shots: int = Field(..., ge=1, description="Number of shots")
    
    # Dice results
    hits: int = Field(0, ge=0)
    wounds: int = Field(0, ge=0)
    saves_failed: int = Field(0, ge=0)
    damage_dealt: int = Field(0, ge=0)
    models_killed: int = Field(0, ge=0)


class ChargeAction(BaseAction):
    """A charge action."""
    
    action_type: ActionType = ActionType.CHARGE
    
    # Target(s)
    targets: list[UnitReference] = Field(..., min_length=1, description="Charge targets")
    
    # Dice
    charge_roll: tuple[int, int] = Field(..., description="2D6 charge roll")
    distance_needed: float = Field(..., ge=0, description="Distance to closest target")
    
    # Result
    made_charge: bool = False


class FightAction(BaseAction):
    """A fight (melee) action."""
    
    action_type: ActionType = ActionType.FIGHT
    
    # Target
    target: UnitReference = Field(..., description="Unit being fought")
    
    # Weapon info
    weapon_name: str = Field(..., description="Melee weapon used")
    attacks: int = Field(..., ge=1, description="Number of attacks")
    
    # Dice results
    hits: int = Field(0, ge=0)
    wounds: int = Field(0, ge=0)
    saves_failed: int = Field(0, ge=0)
    damage_dealt: int = Field(0, ge=0)
    models_killed: int = Field(0, ge=0)


# Union type for all actions
Action = Union[MoveAction, ShootAction, ChargeAction, FightAction]
