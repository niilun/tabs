from .base import BaseUnit
from units import register_new_unit

import logging
from random import randint

@register_new_unit
class ShieldBearer(BaseUnit):
    def __init__(self):
        self.unit_name = 'Shield Bearer'
        self.description = 'The Shield Bearer is a heavy unit. While lacking in physical power, its Bulwark ability shields its teammates from harm.'
        self.abilities = ['Defend', 'Bulwark']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.type = 'Heavy'
        self.attack_style = 'Melee'
        self.attributes = ['Shielded']
        self.effects = {}
        self.max_health = 300
        self.current_health = self.max_health
        self.armor = 0
        self.base_accuracy = 80
        self.accuracy = 100
        self.attack_damage = 20
        self.current_attack_damage = self.attack_damage
    
    def ability_bulwark(self, allies: dict, current_unit_position: int):
        '''
        ABILITY: Bulwark

        The Shield Bearer takes the charge, boosting its own and its teammates' armor by the set boost value!
        '''
        armor_boost_value = 80

        self.armor += armor_boost_value
        try:
            allies[current_unit_position - 1].armor += armor_boost_value
        except Exception:
            pass
        try:
            allies[current_unit_position + 1].armor += armor_boost_value
        except Exception:
            pass

        result = f'The {self.unit_name} boosts its own and its teammates\' armor by {armor_boost_value}!'

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
        
        if randint(1, 10) == 1 and self.can_use_abilities:
            return self.ability_bulwark(allies, current_unit_position)
        else:
            return self.attack(target, self.current_attack_damage)