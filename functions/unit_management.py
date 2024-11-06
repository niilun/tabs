import logging

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

        To be considered valid, the unit needs to have it's own
        current_health, max_health, attack_damage and armor. Also,
        it should have a take_turn method which defines it's AI.

        A unit does not necessarily have to interact with it's armor or max_health
        (though other units may), but the variable needs to exist for unit combat
        to take place correctly, even if it's at 0.

        First, if the unit is in a different file, 
        make sure to import it in unit_management.py.
        
        Then, add a new elif statement with the unit's name and instantiate
        that unit to the 'created_unit' variable.
    '''
    from functions.window_management import display_error_window
    global next_available_id, unit_counter

    if unit not in get_all_units():
        raise Exception('Unit not in units_list')
    
    if unit_counter >= max_units_on_field:
        display_error_window('The maximum number of units on the field at one time is 10!')
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

    # TODO: Remove after UI overhaul (why debug when can have big image)
    logging.debug(f'''New unit lists:
                      Team 1: {active_units_team_1}
                      Team 2: {active_units_team_2}''')

def take_next_action():
    '''Internal function'''
    global turn_counter, unit_counter
    turn_taken = False

    # No fights can happen between empty teams
    if (active_units_team_1 and not active_units_team_2) or (active_units_team_2 and not active_units_team_1) or (not active_units_team_1 and not active_units_team_2):
        raise Exception
    
    # Reset to a new turn cycle if all turns exhausted
    if turn_counter > len(active_units_team_1) + len(active_units_team_2):
        turn_counter = 1
    
    if turn_counter <= len(active_units_team_1) and not turn_taken:
        logging.debug(f'Unit on team 1 turn counter {turn_counter} is taking turn')
        active_units_team_1[turn_counter - 1].take_turn(active_units_team_2)
        turn_counter += 1
        turn_taken = True

    if turn_counter <= len(active_units_team_1) + len(active_units_team_2) and not turn_taken:
        logging.debug(f'Unit on team 2 turn counter {turn_counter} is taking turn')
        active_units_team_2[turn_counter - len(active_units_team_1) - 1].take_turn(active_units_team_1)
        turn_counter += 1
        turn_taken = True

    cleanup_units()

def cleanup_units():
    '''Internal function'''
    global next_available_id, unit_counter, active_units_team_1, active_units_team_2

    for unit in active_units_team_1.copy():
        if unit.current_health <= 0:
            if unit.id == next_available_id:
                next_available_id -= 1
            try:
                logging.debug(f'Unit {unit.unit_name} (ID: {unit.id}) dead, removing')
            except Exception:
                logging.debug(f'Unit <name missing> (ID: {unit.id}) dead, removing')
            unit_counter -= 1
            active_units_team_1.remove(unit)

    for unit in active_units_team_2.copy():
        if unit.current_health <= 0:
            if unit.id == next_available_id:
                next_available_id -= 1
            try:
                logging.debug(f'Unit {unit.unit_name} (ID: {unit.id}) dead, removing')
            except Exception:
                logging.debug(f'Error when parsing Unit name or ID but it is dead, removing')
            unit_counter -= 1
            active_units_team_2.remove(unit)

def get_all_units():
    '''
    Reads text from the "units_list" file (file location is hard-coded). Used to display help messages,
    show them in the selection dropdown and load units on game start.

    FILE FORMATTING
    
        unit1, unit2, unit3 (separated by a comma and a space) without newlines.
    '''
    try:
        with open('units_list', 'r') as f:
            return f.readline().split(', ')
    except FileNotFoundError:
        raise FileNotFoundError('units_list does not exist')

def get_unit_eras():
    '''
    Reads text from the "eras_list" file (file location is hard-coded). Used to display help messages,
    categorize units and load eras on game start.

    FILE FORMATTING
    
        era1, era2, era3 (separated by a comma and a space) without newlines.
    '''
    try:
        with open('eras_list', 'r') as f:
            return f.readline().split(', ')
    except FileNotFoundError:
        raise FileNotFoundError('eras_list does not exist')