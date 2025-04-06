from .base import *

class infantry(base_unit):
    def __init__(self):
        self.unit_name = "Infantry"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 150
        self.max_health = 150
        self.armor = 0
        self.attack_damage = 75