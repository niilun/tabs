from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class LineInfantry(BaseUnit):
    def __init__(self):
        self.unit_name = "Line Infantry"
        self.abilities = ['Attack', 'Defend!']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.attributes = []
        self.effects = {}
        self.max_health = 125
        self.current_health = self.max_health
        self.armor = 0
        self.attack_damage = 65
        self.current_attack_damage = self.attack_damage