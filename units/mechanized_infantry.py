from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class MechanizedInfantry(BaseUnit):
    def __init__(self):
        self.unit_name = "Mechanized Infantry"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 200
        self.max_health = 200
        self.armor = 0
        self.attack_damage = 85