import logging, os

from functions.window_management import display_unit_max_reached

from units.ancient import *
from units.classical import *

# Current number of units active
next_available_id = 1
turn_counter = 1

max_units_on_field = 10

active_units_team_1 = []
active_units_team_2 = []

def create_unit(unit, team):
    global next_available_id
    
    if unit not in get_all_units():
        raise Exception('Unit not in units_list')
    
    if next_available_id >= max_units_on_field:
        display_unit_max_reached()
        raise Exception('Max units on field')

    if unit == 'warrior':
        created_unit = Warrior(next_available_id)
    elif unit == 'spearman':
        created_unit = Spearman(next_available_id)
    
    if team == 1:
        active_units_team_1.append(created_unit)
    else:
        active_units_team_2.append(created_unit)
    
    logging.debug(f'Created unit {unit} ID {next_available_id}')
    next_available_id = next_available_id + 1

    logging.debug(f'''New unit lists:
                      Team 1: {active_units_team_1}
                      Team 2: {active_units_team_2}''')

def take_next_action():
    global turn_counter

    if (active_units_team_1 and not active_units_team_2) or (active_units_team_2 and not active_units_team_1) or (not active_units_team_1 and not active_units_team_2):
        raise Exception('Units do not have an enemy to fight')
    
    if turn_counter > len(active_units_team_1) + len(active_units_team_2):
        turn_counter = 1
    
    if active_units_team_1:
        if turn_counter <= len(active_units_team_1):
            logging.debug(f'Unit on team 1 turn counter {turn_counter} is taking turn')
            active_units_team_1[turn_counter - 1].take_turn(active_units_team_2)
            turn_counter = turn_counter + 1
            return

    if active_units_team_2:
        if turn_counter <= len(active_units_team_1) + len(active_units_team_2):
            logging.debug(f'Unit on team 2 turn counter {turn_counter} is taking turn')
            active_units_team_2[turn_counter - len(active_units_team_1) - 1].take_turn(active_units_team_1)
            turn_counter = turn_counter + 1
            return

def get_all_units():
    # Formatting in-file: unit1, unit2, unit3 (separated by ',' and a space)
    with open('units_list', 'r') as f:
        all_units = f.readline().split(', ')
    return all_units

def get_unit_eras():
    # Formatting in-file: era1, era2, era3 (separated by ',' and a space)
    with open('eras_list', 'r') as f:
        return f.readline().split(', ')