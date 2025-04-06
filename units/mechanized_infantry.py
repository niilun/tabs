from .base import *

class mechanized_infantry(base_unit):
    def __init__(self):
        self.unit_name = "Mechanized Infantry"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.effects = {}
        self.current_health = 200
        self.max_health = 200
        self.armor = 0
        self.attack_damage = 85