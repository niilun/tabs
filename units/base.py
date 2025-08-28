import logging
from random import randint

from game.errors import EffectNotFound
from game.mechanics.status_effects import status_effects

class BaseUnit():
    '''
    Base model for units, does not have stats.

    DO NOT modify it's stats or add new abilities (because it'll change all units based off it), instead create a new unit inheriting from base_unit.
    '''
    def __init__(self):
        self.unit_name = "Base unit"
        self.abilities = ['Attack', 'Defend!']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.attributes = []
        self.effects = {}
        self.max_health = 1
        self.current_health = self.max_health
        self.armor = 0
        self.accuracy = 100
        self.attack_damage = 0
        self.current_attack_damage = self.attack_damage

    def apply_effect(self, effect):
        if effect not in status_effects.__members__.values():
            raise EffectNotFound(effect)
        self.effects[effect] = 3
        logging.debug(f'{self.unit_name} is now {effect.value[0].title()}!')
    
    def handle_effects(self):
        # Reset all statuses (they get reapplied if effects still persist)
        self.accuracy = 100
        self.current_attack_damage = self.attack_damage
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True

        # Every turn effects tick down by 1
        for effect_name in list(self.effects.keys()):
            # First apply effects, then tick them down
            match effect_name:
                case status_effects.BURN:
                    self.current_health -= 20
                    logging.debug(f'{self.unit_name} burned for 20 damage!')
                case status_effects.POISON:
                    self.current_health -= 20
                    logging.debug(f'{self.unit_name} took 20 damage from poison!')
                case status_effects.VENOM:
                    # Venom base damage is 30, upped by 5 for every turn remaining on the counter
                    damage = 30 + (5 * self.effects[effect_name])
                    self.current_health -= damage
                    logging.debug(f'{self.unit_name} took {damage} damage from venom!')
                case status_effects.BLEEDING:
                    self.current_attack_damage -= 15
                    self.current_health -= 10
                    logging.debug(f'{self.unit_name} bled for 10 damage, and its attack power is reduced by 15!')
                case status_effects.STUNNED:
                    self.is_able_to_act = False
                    logging.debug(f'{self.unit_name} is stunned! It can\'t act for this turn!')
                case status_effects.FROZEN:
                    self.is_able_to_act = False
                    logging.debug(f'{self.unit_name} is frozen! It can\'t act for this turn!')
                case status_effects.DEFENCELESS:
                    self.can_defend = False
                    self.armor = 0
                    logging.debug(f'{self.unit_name} is defenceless! It can\'t use \'Defend\' and its armor is broken!')
                case status_effects.DROWSY:
                    self.apply_effect(status_effects.SLEEPY)
                    self.effects.pop(effect_name)
                    logging.debug(f'{self.unit_name} is drowsy! it\'s getting sleepy...')
                    continue
                case status_effects.SLEEPY:
                    self.apply_effect(status_effects.ASLEEP)
                    self.effects.pop(effect_name)
                    logging.debug(f'{self.unit_name} is sleepy! it\'s drifting asleep...')
                    continue
                case status_effects.ASLEEP:
                    self.is_able_to_act = False
                    logging.debug(f'{self.unit_name} is asleep! it\'s unable to act for this turn!')
                case status_effects.CONFUSED:
                    self.accuracy -= 20
                    logging.debug(f'{self.unit_name} is confused! its accuracy is reduced by 20%!')
                case status_effects.BLINDED:
                    self.accuracy -= 50
                    logging.debug(f'{self.unit_name} is confused! its accuracy is reduced by 50%!')
                case status_effects.SILENCED:
                    self.can_use_abilities = False
                    logging.debug(f'{self.unit_name} is silenced! it cannot use any abilities!')
            self.effects[effect_name] -= 1

            if self.effects[effect_name] == 0:
                self.effects.pop(effect_name)

    def take_turn(self, enemies: dict):
        '''
        Default AI

        Tries to use Defend (although randomly) if HP is lower than 50%, otherwise attacks lowest HP unit
        '''

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
        
        return self.attack(target, self.current_attack_damage)
    
    def attack(self, target, damage: int):
        # Clamp accuracy to 100
        accuracy = max(1, min(100, self.accuracy))
        if randint(1, 100) <= accuracy:
            target.get_attacked(damage)
            result = f'{self.unit_name} attacked unit {target.unit_name}, dealing {self.attack_damage} damage.'
            logging.debug(result)
            return result
        else:
            result = f'{self.unit_name} missed its attack!'
            logging.debug(result)
            return result

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