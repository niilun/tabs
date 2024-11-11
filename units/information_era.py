from .base import *

# +-------------------------+
# |  information era units  |
# +-------------------------+

class Mechanized_Infantry(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Mechanized Infantry"
        self.id = id
        self.current_health = 200
        self.max_health = 200
        self.armor = 0
        self.attack_damage = 85