from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class LineInfantry(BaseUnit):
    def __init__(self):
        self.unit_name = "Line Infantry"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 125
        self.max_health = 125
        self.armor = 0
        self.attack_damage = 65