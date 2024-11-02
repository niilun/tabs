import logging

from functions.window_management import display_unit_max_reached

from units.ancient import *
from units.classical import *

# Management counters
next_available_id = 1
unit_counter = 1
turn_counter = 1

max_units_on_field = 10

active_units_team_1 = []
active_units_team_2 = []

def create_unit(unit, team):
    '''
    Creates a unit using input from the tkinter window interface, called when pressing
    'Summon' on either team.

    ADDING A NEW UNIT

        First, if the unit is in a new era (different file),
        import that at the top.

        Then, add a new elif statement with the unit's name and instantiate
        that unit to 'created_unit'.
    '''
    global next_available_id, unit_counter

    if unit not in get_all_units():
        raise Exception('Unit not in units_list')
    
    if unit_counter >= max_units_on_field:
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
    next_available_id += 1
    unit_counter += 1

    logging.debug(f'''New unit lists:
                      Team 1: {active_units_team_1}
                      Team 2: {active_units_team_2}''')

def take_next_action():
    '''Internal function'''
    global turn_counter, unit_counter

    if (active_units_team_1 and not active_units_team_2) or (active_units_team_2 and not active_units_team_1) or (not active_units_team_1 and not active_units_team_2):
        raise Exception('Units do not have an enemy to fight')
    
    if turn_counter > len(active_units_team_1) + len(active_units_team_2):
        turn_counter = 1
    
    if active_units_team_1:
        if turn_counter <= len(active_units_team_1):
            logging.debug(f'Unit on team 1 turn counter {turn_counter} is taking turn')
            active_units_team_1[turn_counter - 1].take_turn(active_units_team_2)
            turn_counter += 1
            cleanup_units()
            return

    if active_units_team_2:
        if turn_counter <= len(active_units_team_1) + len(active_units_team_2):
            logging.debug(f'Unit on team 2 turn counter {turn_counter} is taking turn')
            active_units_team_2[turn_counter - len(active_units_team_1) - 1].take_turn(active_units_team_1)
            turn_counter += 1
            cleanup_units()
            return

def cleanup_units():
    '''Internal function'''
    global next_available_id, unit_counter, active_units_team_1, active_units_team_2
    
    active_1_copy = active_units_team_1.copy()
    active_2_copy = active_units_team_2.copy()

    for unit in active_1_copy:
        if unit.current_health <= 0:
            if unit.id == next_available_id:
                next_available_id -= 1
            logging.debug(f'Unit {unit.unit_name} (ID: {unit.id}) dead, removing')
            unit_counter -= 1
            active_units_team_1.remove(unit)

    for unit in active_2_copy:
        if unit.current_health <= 0:
            if unit.id == next_available_id:
                next_available_id -= 1
            logging.debug(f'Unit {unit.unit_name} (ID: {unit.id}) dead, removing')
            unit_counter -= 1
            active_units_team_2.remove(unit)

def get_all_units():
    '''
    Reads text from the "units_list" file (file location is hard-coded). Used to display help messages,
    show them in the selection dropdown and load units on game start.

    FORMATTING
    
        unit1, unit2, unit3 (separated by a comma and a space) without newlines.
    '''
    with open('units_list', 'r') as f:
        all_units = f.readline().split(', ')
    return all_units

def get_unit_eras():
    '''
    Reads text from the "eras_list" file (file location is hard-coded). Used to display help messages,
    categorize units and load eras on game start.

    FORMATTING
    
        era1, era2, era3 (separated by a comma and a space) without newlines.
    '''
    with open('eras_list', 'r') as f:
        return f.readline().split(', ')