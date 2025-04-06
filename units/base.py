import logging
from random import randint

class base_unit():
    '''
    Base model for units, does not have stats.

    DO NOT modify it's stats or add new abilities (because it'll change all units based off it), instead create a new unit inheriting from base_unit.
    '''
    def __init__(self):
        self.unit_name = "Base unit"
        self.abilities = ['Attack', 'Defend!']
        self.attributes = []
        self.current_health = 1
        self.max_health = 1
        self.armor = 0
        self.attack_damage = 0
        self.effects = {}

    def take_turn(self, enemies: dict):
        '''
        Default AI

        Tries to use Defend (although randomly) if HP is lower than 50%, otherwise attacks lowest HP unit
        '''
        if self.current_health < self.max_health/2 and self.armor < 10 and randint(1, 10) <= 2:
            self.ability_defend()
            return
        
        # Target is the enemy with lowest HP. If there are 2+ units with the same HP, the first
        min_health_in_enemy_team = min([enemy.current_health for enemy in enemies.values() if enemy != None])
        for enemy in enemies.values():
            if enemy == None:
                pass
            elif enemy.current_health == min_health_in_enemy_team:
                target = enemy
        target.get_attacked(self.attack_damage)
        
        logging.debug(f"{self.unit_name} attacked unit {target.unit_name}, dealing {self.attack_damage} damage. (HP now {target.current_health})")

    def get_attacked(self, damage):
        '''
        Default course of action when getting attacked

        Tries to break armor, otherwise attacks
        Excess damage is nulled!
        '''
        if self.armor > 0:
            if self.armor - damage <= 0:
                self.armor = 0
                logging.debug(f"{self.unit_name}'s armor has been broken!")
                return
            self.armor -= damage
            return
        
        self.current_health -= damage

    def ability_defend(self):
        '''
        Default Defend

        Adds 30 armor to self, which tanks in place of HP on attack.
        '''
        self.armor += 30
        logging.debug(f'{self.unit_name} used Defend! (armor now {self.armor})')