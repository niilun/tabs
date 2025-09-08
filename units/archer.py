from .base import BaseUnit
from units import register_new_unit

import logging
from random import choice, randint

@register_new_unit
class Musketman(BaseUnit):
    def __init__(self):
        self.unit_name = 'Archer'
        self.description = 'A ranged unit skilled at attacking enemies from a distance. Its Volley ability allows it to hit multiple units at once!'
        self.abilities = ['Defend', 'Volley']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.type = 'Light'
        self.attack_style = 'Ranged'
        self.attributes = []
        self.effects = {}
        self.max_health = 110
        self.current_health = self.max_health
        self.armor = 0
        self.base_accuracy = 100
        self.accuracy = 100
        self.attack_damage = 55
        self.current_attack_damage = self.attack_damage
    
    def ability_volley(self, enemies: dict, target):
        '''
        ABILITY: Volley
        
        Deals base attack damage damage to target, with the arrow bouncing to another target for 75%, and to another for 50% damage.
        Attributes do not apply modifiers for the second and third target.
        '''
        volley_first_recoil_damage = self.current_attack_damage * 0.75
        volley_second_recoil_damage = self.current_attack_damage * 0.50

        # create a list from enemies and remove the first target
        available_targets = [enemy for enemy in enemies.values() if enemy is not None and enemy != target]

        # find a second and third target if available
        first_target = choice(available_targets) if available_targets else None
        remaining_targets = [enemy for enemy in available_targets if enemy != first_target]
        second_target = choice(remaining_targets) if remaining_targets else None

        self.attack(target, self.current_attack_damage)
        if first_target:
            self.attack(first_target, volley_first_recoil_damage)
        if second_target:
            self.attack(second_target, volley_second_recoil_damage)

        result = f'{self.unit_name} used Volley to deal {int(self.current_attack_damage)} damage to {target.unit_name}'
        if first_target:
            result += f', recoiling to {first_target.unit_name} for {int(volley_first_recoil_damage)}'
        if second_target:
            result += f' and {second_target.unit_name} for {int(volley_second_recoil_damage)} damage!'
        else:
            result += '!'
        logging.debug(result)
        return result
    
    def take_turn(self, allies: dict, enemies: dict, current_unit_position: int):
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
        
        self.handle_self_attributes()
        self.handle_attributes(target)
        self.handle_type(target)
        
        if randint(1, 4) == 1 and self.can_use_abilities:
            return self.ability_volley(enemies, target)
        else:
            return self.attack(target, self.current_attack_damage)