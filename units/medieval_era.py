from .base import *

# +----------------------+
# |  medieval era units  |
# +----------------------+

class man_at_arms(base_unit):
    def __init__(self, id):
        self.unit_name = "Man-at-Arms"
        self.id = id
        self.current_health = 100
        self.max_health = 100
        self.armor = 0
        self.attack_damage = 45