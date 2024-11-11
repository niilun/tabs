from .base import *

# +-------------------------+
# |  renaissance era units  |
# +-------------------------+

class Musketman(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Musketman"
        self.id = id
        self.current_health = 110
        self.max_health = 110
        self.armor = 0
        self.attack_damage = 55