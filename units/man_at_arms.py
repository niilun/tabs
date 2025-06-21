from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class ManAtArms(BaseUnit):
    def __init__(self):
        self.unit_name = "Man-at-Arms"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 100
        self.max_health = 100
        self.armor = 0
        self.attack_damage = 45