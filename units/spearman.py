from .base import *
import logging

class spearman(base_unit):
    def __init__(self):
        self.unit_name = 'Spearman'
        self.attributes = []
        self.effects = {}
        self.current_health = 70
        self.max_health = 70
        self.armor = 0
        self.attack_damage = 35