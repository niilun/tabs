from .base import *

# +--------------------+
# |  modern era units  |
# +--------------------+

class Infantry(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Infantry"
        self.id = id
        self.current_health = 150
        self.max_health = 150
        self.armor = 0
        self.attack_damage = 75