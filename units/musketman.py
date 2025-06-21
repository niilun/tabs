from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class Musketman(BaseUnit):
    def __init__(self):
        self.unit_name = "Musketman"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 110
        self.max_health = 110
        self.armor = 0
        self.attack_damage = 55