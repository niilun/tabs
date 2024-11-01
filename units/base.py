import logging

# Base model for human units (functions to override)
class BaseUnit():
    def __init__(self, id):
        self.unit_name = "Base unit"
        self.id = id
        self.armor = 0
        self.current_health = 1
        self.max_health = 1
        self.attack_damage = 0
    
    # Default AI
    # Tries to use Defend if HP is lower than 50%, otherwise attacks lowest HP unit
    def take_turn(self, enemies):
        if self.current_health < self.max_health/2:
            self.ability_defend()
            return
        target = [enemy for enemy in enemies if enemy.current_health == min([enemy.current_health for enemy in enemies])]
        logging.debug(f"{self.unit_name} attacked unit ID {target.id} ({target.unit_name}), dealing {self.attack_damage} damage.")
        self.ability_attack(target)

    # Default Attack
    # Tries to break armor otherwise attacks
    def ability_attack(self, target):
        if target.armor > 0:
            target.armor -= self.attack_damage
            return
        target.health -= self.attack_damage

    # Default Defend
    # Adds 20 armor to self
    def ability_defend(self):
        self.armor += 20
        logging.debug(f'{self.unit_name} used Defend! (armor now {self.armor})')