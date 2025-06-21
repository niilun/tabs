from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class Spearman(BaseUnit):
    def __init__(self):
        self.unit_name = "Spearman"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 70
        self.max_health = 70
        self.armor = 0
        self.attack_damage = 25