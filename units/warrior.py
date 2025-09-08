from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class Warrior(BaseUnit):
    def __init__(self):
        self.unit_name = 'Warrior'
        self.description = 'A simple warrior unit, a balanced mix of ancient era offence and defence.'
        self.abilities = ['Defend']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.type = 'Medium'
        self.attack_style = 'Melee'
        self.attributes = []
        self.effects = {}
        self.max_health = 50
        self.current_health = self.max_health
        self.armor = 0
        self.base_accuracy = 100
        self.accuracy = 100
        self.attack_damage = 20
        self.current_attack_damage = self.attack_damage