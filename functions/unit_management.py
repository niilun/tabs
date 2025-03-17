import logging

from units.ancient_era import *
from units.classical_era import *
from units.medieval_era import *
from units.renaissance_era import *
from units.industrial_era import *
from units.modern_era import *
from units.atomic_era import *
from units.information_era import *

# Maps used when the user interacts with the game (add your units and/or eras here)
all_units_map = {
    'warrior': warrior,
    'spearman': spearman,
    'man at arms': man_at_arms,
    'musketman': musketman,
    'infantry': infantry,
    'line infantry': line_infantry,
    'mechanized infantry': mechanized_infantry
}

# Maps units to their specific eras (used in the future maybe, in a dropdown menu to select units)
all_eras_map = {
    'ancient': warrior,
    'classical': spearman,
    'medieval': man_at_arms,
    'renaissance': musketman,
    'industrial': line_infantry,
    'modern': infantry,
    'atomic': None,
    'information': mechanized_infantry
}

# Unit management counters
next_available_id = 1
unit_counter = 1
turn_counter = 1

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
        
        Then, add the unit to all_units_map with it's user-friendly name.
    '''
    global next_available_id, unit_counter

    unit = unit.lower()

    if unit not in all_units_map:
        raise Exception('Unit does not exist or is not declared!')
    
    created_unit = all_units_map[unit.lower()](next_available_id)

    if team == 1:
        if len(active_units_team_1) >= 5:
            raise Exception('Team 1 is full!')
        active_units_team_1.append(created_unit)
    elif team == 2:
        if len(active_units_team_2) >= 5:
            raise Exception('Team 2 is full!')
        active_units_team_2.append(created_unit)
    else:
        raise Exception(f"Invalid team call {team}")
    
    logging.debug(f'Created unit {unit} ID {next_available_id}')
    next_available_id += 1
    unit_counter += 1

    logging.debug(f'''New unit lists:
        Team 1: {active_units_team_1}
        Team 2: {active_units_team_2}''')

def take_next_action():
    '''Calculates the next unit that's supposed to take it's turn and runs it's take_turn() method'''
    global turn_counter, unit_counter
    turn_taken = False

    # No fights can happen between empty teams
    if (active_units_team_1 and not active_units_team_2) or (active_units_team_2 and not active_units_team_1) or (not active_units_team_1 and not active_units_team_2):
        raise Exception('No fights can happen between empty teams! \nAdd some units to both before continuing to take turns.')
    
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
    '''Checks for dead units in both teams and removes them from the game'''
    global next_available_id, unit_counter, active_units_team_1, active_units_team_2
    
    # Use copies when iterating
    for unit in active_units_team_1.copy():
        if unit.current_health <= 0:
            if unit.id == next_available_id:
                next_available_id -= 1
            logging.info(f'Unit {unit.unit_name} (ID: {unit.id}) dead, removing')
            unit_counter -= 1
            active_units_team_1.remove(unit)

    for unit in active_units_team_2.copy():
        if unit.current_health <= 0:
            if unit.id == next_available_id:
                next_available_id -= 1
            logging.info(f'Unit {unit.unit_name} (ID: {unit.id}) dead, removing')
            unit_counter -= 1
            active_units_team_2.remove(unit)