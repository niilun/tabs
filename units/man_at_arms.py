from .base import *

class man_at_arms(base_unit):
    def __init__(self):
        self.unit_name = "Man-at-Arms"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 100
        self.max_health = 100
        self.armor = 0
        self.attack_damage = 45