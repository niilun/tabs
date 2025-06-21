from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class Infantry(BaseUnit):
    def __init__(self):
        self.unit_name = "Infantry"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 150
        self.max_health = 150
        self.armor = 0
        self.attack_damage = 75