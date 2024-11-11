from .base import *

# +----------------------+
# |  medieval era units  |
# +----------------------+

class Man_at_Arms(BaseUnit):
    def __init__(self, id):
        self.unit_name = "Man-at-Arms"
        self.id = id
        self.current_health = 100
        self.max_health = 100
        self.armor = 0
        self.attack_damage = 45