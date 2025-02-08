from enum import Enum

class status_effects(Enum):
    """
    These effects can be applied to units during gameplay and have various impacts on their abilities and actions.

    They stop affecting the next turn after they are cleared
    off the unit's active effects, or after a specific period
    of time.

    IMPORTANT: units need to check for active effects on their own
    when their turn is called and apply the effects they choose to
    themselves.
    """

    # Statuses that inflict self damage
    BURN = ["Burned", "takes damage every turn"]
    POISON = ["Poisoned", "takes damage every turn"]
    VENOM = ["Envenomed", "takes stronger damage every turn"]
    CONFUSED = ["Confused", "takes damage when attacking"]
    BLEEDING = ["Bleeding", "loses health gradually"]

    # Statuses that prevent actions
    DROWSY = ["Drowsy", "getting drowsy..."]
    SLEEPY = ["Sleepy", "about to go Asleep!"]
    ASLEEP = ["Asleep", "cannot act"]

    STUN = ["Stunned", "cannot act"]
    FROZEN = ["Frozen", "cannot act and takes increased damage from physical attacks"]
    PARALYZED = ["Paralyzed", "has a chance to fail actions"]
    DEFENCELESS = ["Defenceless", "cannot 'Defend' and their armor gets penetrated by attacks"]
    
    # Statuses that affect specific actions
    BLINDED = ["Dazed", "may fail attacks"]
    SILENCED = ["Silenced", "cannot use abilities"]