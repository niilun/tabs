from .base import *

# +----------------------+
# |  medieval era units  |
# +----------------------+

class man_at_arms(base_unit):
    def __init__(self):
        self.unit_name = "Man-at-Arms"
        self.current_health = 100
        self.max_health = 100
        self.armor = 0
        self.attack_damage = 45