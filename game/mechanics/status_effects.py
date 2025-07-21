from enum import Enum

class status_effects(Enum):
    """
    These effects can be applied to units and have various impacts on their abilities and actions.

    Effects are applied using a unit's apply_effect() method by passing the effect. A default one exists
    in the base unit class, which applies them for three turns (except a couple). You can override this
    with your own method.
    
    As a standard, effects should stop the next turn after they are cleared
    off the unit's active effects.

    A standardised way of handling effects is provided in the base unit class with
    the handle_effects function, however you can override it with your own.
    """

    # Statuses that inflict self damage
    BURN = ["Burned", "Takes damage every turn"]
    POISON = ["Poisoned", "Takes damage every turn"]
    VENOM = ["Envenomed", "Takes ramping damage every turn"]
    BLEEDING = ["Bleeding", "Loses health gradually"]

    # Statuses that prevent actions

    STUNNED = ["Stunned", "Cannot act"]
    FROZEN = ["Frozen", "Cannot act"]
    DEFENCELESS = ["Defenceless", "Cannot 'Defend' and armor gets broken"]

    # The intent is to have Drowsy -> Sleepy -> Asleep be a weaker version of Stun, as it takes 3 turns to actually take effect.
    DROWSY = ["Drowsy", "Getting drowsy..."]
    SLEEPY = ["Sleepy", "About to go Asleep!"]
    ASLEEP = ["Asleep", "Cannot act"]
    
    # Statuses that affect specific actions
    CONFUSED = ["Confused", "Has reduced accuracy"]
    BLINDED = ["Dazed", "Has highly reduced accuracy"]
    SILENCED = ["Silenced", "Cannot use abilities"]
