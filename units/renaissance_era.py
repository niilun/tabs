from .base import *

# +-------------------------+
# |  renaissance era units  |
# +-------------------------+

class musketman(base_unit):
    def __init__(self):
        self.unit_name = "Musketman"
        self.attributes = []
        self.effects = {}
        self.current_health = 110
        self.max_health = 110
        self.armor = 0
        self.attack_damage = 55