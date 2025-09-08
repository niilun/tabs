from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class Spearman(BaseUnit):
    def __init__(self):
        self.unit_name = 'Spearman'
        self.description = 'The spearman is a basic unit equipped with a long spear, which is very effective against cavalry.'
        self.abilities = ['Defend']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.type = 'Medium'
        self.attack_style = 'Melee'
        self.attributes = ['Anti-Cavalry']
        self.effects = {}
        self.max_health = 70
        self.current_health = self.max_health
        self.armor = 0
        self.base_accuracy = 100
        self.accuracy = 100
        self.attack_damage = 25
        self.current_attack_damage = self.attack_damage