from .base import *
import logging

# +---------------------+
# |  ancient era units  |
# |  TODO: add all      |
# |  units info         |
# +---------------------+

class Warrior(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Warrior"
        self.id = id
        self.current_health = 50
        self.max_health = 50
        self.attack_damage = 20