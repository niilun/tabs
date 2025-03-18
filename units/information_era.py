from .base import *

# +-------------------------+
# |  information era units  |
# +-------------------------+

class mechanized_infantry(base_unit):
    def __init__(self):
        self.unit_name = "Mechanized Infantry"
        self.current_health = 200
        self.max_health = 200
        self.armor = 0
        self.attack_damage = 85