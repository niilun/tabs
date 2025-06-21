from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class Warrior(BaseUnit):
    def __init__(self):
        self.unit_name = "Warrior"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 50
        self.max_health = 50
        self.armor = 0
        self.attack_damage = 20