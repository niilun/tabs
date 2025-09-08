from .base import BaseUnit
from units import register_new_unit

@register_new_unit
class ManAtArms(BaseUnit):
    def __init__(self):
        self.unit_name = 'Man-at-Arms'
        self.description = 'A Man-At-Arms regiment, heavily armored and able to withstand the harshest of attacks with their shields.'
        self.abilities = ['Defend']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.type = 'Heavy'
        self.attack_style = 'Melee'
        self.attributes = ['Shielded']
        self.effects = {}
        self.max_health = 100
        self.current_health = self.max_health
        self.armor = 0
        self.base_accuracy = 100
        self.accuracy = 100
        self.attack_damage = 45
        self.current_attack_damage = self.attack_damage