import logging

from units.ancient_era import *
from units.classical_era import *
from units.medieval_era import *
from units.renaissance_era import *
from units.industrial_era import *
from units.modern_era import *
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

# Unit storage
turn_counter = 1

active_units_t1 = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None
}

active_units_t2 = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None
}

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

    unit = unit.lower()

    if unit not in all_units_map:
        raise Exception('Unit does not exist or is not declared!')
    
    created_unit = all_units_map[unit]()

    if team == 1:
        if get_total_active_units(1) >= 5:
            raise Exception('Team 1 is full!')
        
        logging.debug(f'Created unit {unit} in slot {find_first_available_slot(1)}')
        active_units_t1[find_first_available_slot(1)] = created_unit
    elif team == 2:
        if get_total_active_units(2) >= 5:
            raise Exception('Team 2 is full!')

        logging.debug(f'Created unit {unit} in slot {find_first_available_slot(2)}')
        active_units_t2[find_first_available_slot(2)] = created_unit
    else:
        raise Exception(f"Invalid team call {team}")

    logging.debug(f'''New unit lists:
        Team 1, {get_total_active_units(1)} active: {active_units_t1}
        Team 2, {get_total_active_units(2)} active: {active_units_t2}''')

def take_next_action():
    '''Calculates the next unit that's supposed to take its turn and runs its take_turn() method'''
    global turn_counter
    turn_taken = False

    # No fights can happen between empty teams
    if get_total_active_units(1) == 0 or get_total_active_units(2) == 0:
        raise Exception('No fights can happen between empty teams! \nAdd some units to both before continuing to take turns.')
    
    # Reset to a new turn cycle if all turns exhausted
    if turn_counter > get_total_active_units(1) + get_total_active_units(2):
        turn_counter = 1
    
    if turn_counter <= get_total_active_units(1) and not turn_taken:
        logging.debug(f'Unit on team 1 turn counter {turn_counter} is taking turn')
        active_units_t1[turn_counter].take_turn(active_units_t2)

        turn_counter += 1
        turn_taken = True

    if turn_counter <= get_total_active_units(1) + get_total_active_units(2) and not turn_taken:
        logging.debug(f'Unit on team 2 turn counter {turn_counter} is taking turn')
        active_units_t2[turn_counter - get_total_active_units(1)].take_turn(active_units_t1)

        turn_counter += 1
        turn_taken = True

    cleanup_units()

def cleanup_units():
    '''Checks for dead units in both teams and removes them from the game'''

    # Use copies when iterating
    counter = 1
    for unit in active_units_t1.copy().values():
        if unit == None:
            pass
        elif unit.current_health <= 0:
            logging.info(f'Unit {unit.unit_name} in team 1, slot {counter} dead, removing')
            active_units_t1[counter] = None
        counter += 1

    counter = 1
    for unit in active_units_t2.copy().values():
        if unit == None:
            pass
        elif unit.current_health <= 0:
            logging.info(f'Unit {unit.unit_name} in team 2, slot {counter} dead, removing')
            active_units_t2[counter] = None
        counter += 1

def find_first_available_slot(team: int) -> int:
    counter = 1
    if team == 1:
        for slot in active_units_t1.values():
            if slot == None:
                return counter
            counter += 1
    elif team == 2:
        for slot in active_units_t2.values():
            if slot == None:
                return counter
            counter += 1
    else:
        raise Exception(f'Invalid team call {team} in {__name__}')

def get_total_active_units(team: int) -> int:
    total = 0
    if team == 1:
        for slot in active_units_t1.values():
            if slot != None:
                total += 1
    elif team == 2:
        for slot in active_units_t2.values():
            if slot != None:
                total += 1
    else:
        raise Exception(f'Invalid team call {team} in {__name__}')
    return total