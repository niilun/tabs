import logging
from random import randint

from .base import BaseUnit
from units import register_new_unit

from game.mechanics.status_effects import status_effects

@register_new_unit
class FireWizard(BaseUnit):
    def __init__(self):
        self.unit_name = "Fire Wizard"
        self.abilities = ['Attack', 'Fire Wave', 'Defend!']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.attributes = []
        self.effects = {}
        self.max_health = 120
        self.current_health = self.max_health
        self.armor = 0
        self.accuracy = 100
        self.attack_damage = 70
        self.current_attack_damage = self.attack_damage

    def ability_fire_wave(self, target):
        '''
        ABILITY: Fire Wave

        Deals halved attack damage, but inflicts burn.
        '''

        self.attack(target, self.current_attack_damage * 0.5)
        
        result = f'{self.unit_name} used Fire Wave on {target.unit_name}, dealing {self.attack_damage * 0.5} damage.'
        target.apply_effect(status_effects.BURN)
        logging.debug(result)
        return result

    def take_turn(self, enemies: dict):
        '''
        Fire Wizard AI

        Tries to use Defend (although randomly) if HP is lower than 50%, then runs 25% for Fire Wave, otherwise attacks.
        '''

        self.handle_effects()

        if not self.is_able_to_act:
            return f'{self.unit_name} is not able to act!'
        
        if self.can_defend and self.can_use_abilities:
            if self.current_health < self.max_health/2 and self.armor < 10 and randint(1, 10) <= 2:
                self.ability_defend()
                return f'{self.unit_name} used Defend!'
        
        # Target is the enemy with lowest HP. If there are 2+ units with the same HP, the first from the left is chosen
        min_health_in_enemy_team = min([enemy.current_health for enemy in enemies.values() if enemy != None])
        for enemy in enemies.values():
            if enemy == None:
                pass
            elif enemy.current_health == min_health_in_enemy_team:
                target = enemy
        
        # ABILITY: Fire Wave (25%)
        if randint(1, 4) == 1 and self.can_use_abilities:
            return self.ability_fire_wave(target)
        else:            
            return self.attack(target, self.current_attack_damage)