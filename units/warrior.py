from .base import *

class warrior(base_unit):
    def __init__(self):
        self.unit_name = "Warrior"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 50
        self.max_health = 50
        self.armor = 0
        self.attack_damage = 20