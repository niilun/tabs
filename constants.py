from enum import Enum

class status_effects(Enum):
    """
    These effects can be applied to units and have various impacts on their abilities and actions.

    As a standard, effects stop the next turn after they are cleared
    off the unit's active effects.

    IMPORTANT: units need to check for active effects on their own
    when their turn is called and apply the effects they choose to
    themselves.
    """

    # Statuses that inflict self damage
    BURN = ["Burned", "Takes damage every turn"]
    POISON = ["Poisoned", "Takes damage every turn"]
    VENOM = ["Envenomed", "Takes ramping damage every turn"]
    CONFUSED = ["Confused", "Takes damage when attacking"]
    BLEEDING = ["Bleeding", "Loses health gradually"]

    # Statuses that prevent actions

    STUN = ["Stunned", "Cannot act"]
    FROZEN = ["Frozen", "Cannot act and takes double damage from the next attack, after which the effect is removed"]
    PARALYZED = ["Paralyzed", "May fail actions"]
    DEFENCELESS = ["Defenceless", "Cannot 'Defend' and armor gets penetrated by attacks"]

    # The intent is to have Drowsy -> Sleepy -> Asleep be a weaker version of Stun, as it takes 3 turns to actually take effect.
    DROWSY = ["Drowsy", "Getting drowsy..."]
    SLEEPY = ["Sleepy", "About to go Asleep!"]
    ASLEEP = ["Asleep", "Cannot act"]
    
    # Statuses that affect specific actions
    BLINDED = ["Dazed", "May fail attacks"]
    SILENCED = ["Silenced", "Cannot use abilities"]