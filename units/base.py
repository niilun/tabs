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
        self.abilities = ['Defend']
        self.is_able_to_act = True
        self.can_defend = True
        self.can_use_abilities = True
        self.type = None
        self.attack_style = None
        self.attributes = []
        self.effects = {}
        self.max_health = 1
        self.current_health = self.max_health
        self.armor = 0
        self.base_accuracy = 100
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

        if self.base_accuracy:
            self.accuracy = self.base_accuracy
        
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
                    logging.debug(f'{self.unit_name} is blinded! its accuracy is reduced by 50%!')
                case status_effects.SILENCED:
                    self.can_use_abilities = False
                    logging.debug(f'{self.unit_name} is silenced! it cannot use any abilities!')
            self.effects[effect_name] -= 1

            if self.effects[effect_name] == 0:
                self.effects.pop(effect_name)
        
    def handle_attributes(self, enemy):
        # attributes that affect interactions between self and enemy
        match (self.attributes, enemy.attributes):
            case (self_attributes, enemy_attributes) if 'Anti-Infantry' in self_attributes and 'Infantry' in enemy_attributes:
                self.current_attack_damage *= 1.3
                logging.info(f'{self.unit_name}\'s anti-infantry measures cause it to deal 30% more damage, since {enemy.unit_name} is Infantry!')
            case (self_attributes, enemy_attributes) if 'Anti-Cavalry' in self_attributes and 'Cavalry' in enemy_attributes:
                self.current_attack_damage *= 1.3
                logging.info(f'{self.unit_name} pierces thru {enemy.unit_name}\'s Cavalry, dealing 30% more damage!')
            case _:
                pass
        
    def handle_self_attributes(self):
        if 'Shielded' in self.attributes:
            if self.armor < 15:
                self.armor = 15
                logging.info(f'{self.unit_name} had its armor boosted due to its Shielded attribute')
    
    def handle_type(self, enemy):
        match (self.type, enemy.type):
            case ('Light', 'Heavy'):
                self.current_attack_damage *= 1.25
                logging.info(f'{self.unit_name} manoeuvres around {enemy.unit_name}\'s heavy armor for 25% more damage!')
            case ('Heavy', 'Medium'):
                self.current_attack_damage *= 1.25
                logging.info(f'{self.unit_name} crushes {enemy.unit_name}\'s medium armor for 25% more damage!')
            case ('Medium', 'Light'):
                self.current_attack_damage *= 1.25
                logging.info(f'{self.unit_name} counters {enemy.unit_name}\'s agility for 25% more damage!')
            case _:
                pass

    def take_turn(self, allies: dict, enemies: dict, current_unit_position: int):
        '''
        Default AI

        Tries to use Defend (although randomly) if HP is lower than 50%, otherwise attacks lowest HP unit
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
        
        self.handle_self_attributes()
        self.handle_attributes(target)
        self.handle_type(target)
        
        return self.attack(target, self.current_attack_damage)
    
    def attack(self, target, damage: int):
        # Clamp accuracy to 100
        damage = int(damage)
        accuracy = max(1, min(100, self.accuracy))
        if randint(1, 100) <= accuracy:
            target.get_attacked(damage)
            result = f'{self.unit_name} attacked unit {target.unit_name}, dealing {damage} damage.'
            logging.debug(result)
            return result
        else:
            result = f'{self.unit_name} missed its attack!'
            logging.debug(result)
            return result

    def get_attacked(self, damage):
        '''
        Default course of action when getting attacked

        If armor exists, remove it and send the remaining to the HP bar.
        '''
        if self.armor > 0:
            if self.armor - damage <= 0:
                remainder = damage - self.armor
                self.armor = 0
                self.current_health -= remainder
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