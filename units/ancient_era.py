from .base import *

# +---------------------+
# |  ancient era units  |
# +---------------------+

class Warrior(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Warrior"
        self.id = id
        self.current_health = 50
        self.max_health = 50
        self.armor = 0
        self.attack_damage = 20