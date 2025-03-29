from .base import *

# +------------------------+
# |  industrial era units  |
# +------------------------+

class line_infantry(base_unit):
    def __init__(self):
        self.unit_name = "Line Infantry"
        self.attributes = []
        self.effects = {}
        self.current_health = 125
        self.max_health = 125
        self.armor = 0
        self.attack_damage = 65