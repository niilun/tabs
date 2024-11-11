from .base import *

# +------------------------+
# |  industrial era units  |
# +------------------------+

class Line_Infantry(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Line Infantry"
        self.id = id
        self.current_health = 125
        self.max_health = 125
        self.armor = 0
        self.attack_damage = 65