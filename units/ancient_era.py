from .base import *

# +---------------------+
# |  ancient era units  |
# +---------------------+

class warrior(base_unit):
    def __init__(self):
        self.unit_name = "Warrior"
        self.current_health = 50
        self.max_health = 50
        self.armor = 0
        self.attack_damage = 20