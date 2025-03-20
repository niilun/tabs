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

active_units_team_1 = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None
}

active_units_team_2 = {
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
    from functions.window_management import update_scoreboard
    unit = unit.lower()

    if unit not in all_units_map:
        raise Exception('Unit does not exist or is not declared!')
    
    created_unit = all_units_map[unit]()

    if team == 1:
        if get_total_active_units(1) >= 5:
            raise Exception('Team 1 is full!')
        
        logging.debug(f'Created unit {unit} in slot {find_first_available_slot(1)}')
        active_units_team_1[find_first_available_slot(1)] = created_unit
    elif team == 2:
        if get_total_active_units(2) >= 5:
            raise Exception('Team 2 is full!')

        logging.debug(f'Created unit {unit} in slot {find_first_available_slot(2)} on team {team}')
        active_units_team_2[find_first_available_slot(2)] = created_unit
    else:
        raise Exception(f"Invalid team call {team}")

    update_scoreboard()

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
        try:
            active_units_team_1[turn_counter].take_turn(active_units_team_2)
        except Exception:
            # If a unit dies and it's turn is the one coming up we account for it by +1-ing the counter
            turn_counter += 1

        turn_counter += 1
        turn_taken = True

    if turn_counter <= get_total_active_units(1) + get_total_active_units(2) and not turn_taken:
        logging.debug(f'Unit on team 2 turn counter {turn_counter} is taking turn')
        try:
            active_units_team_2[turn_counter - get_total_active_units(1)].take_turn(active_units_team_1)
        except Exception:
            # If a unit dies and it's turn is the one coming up we account for it by +1-ing the counter
            turn_counter += 1

        turn_counter += 1
        turn_taken = True

    cleanup_units()

def cleanup_units():
    '''Checks for dead units in both teams and removes them from the game'''
    from functions.window_management import update_scoreboard
    
    # Use copies when iterating
    counter = 1
    for unit in active_units_team_1.copy().values():
        if unit == None:
            pass
        elif unit.current_health <= 0:
            logging.info(f'Unit {unit.unit_name} in slot {counter} in team 1 dead, removing')
            active_units_team_1[counter] = None
        counter += 1

    counter = 1
    for unit in active_units_team_2.copy().values():
        if unit == None:
            pass
        elif unit.current_health <= 0:
            logging.info(f'Unit {unit.unit_name} in slot {counter} in team 2 dead, removing')
            active_units_team_2[counter] = None
        counter += 1
    update_scoreboard()

def find_first_available_slot(team: int) -> int:
    '''Finds the first available slot going from left to right for team 1 or 2.'''
    counter = 1
    if team == 1:
        for slot in active_units_team_1.values():
            if slot == None:
                return counter
            counter += 1
    elif team == 2:
        for slot in active_units_team_2.values():
            if slot == None:
                return counter
            counter += 1
    else:
        raise Exception(f'Invalid team call {team} in {__name__}')

def get_total_active_units(team: int) -> int:
    '''Gets the total number of active units for team 1 or 2.'''
    total = 0
    if team == 1:
        for slot in active_units_team_1.values():
            if slot != None:
                total += 1
    elif team == 2:
        for slot in active_units_team_2.values():
            if slot != None:
                total += 1
    else:
        raise Exception(f'Invalid team call {team} in {__name__}')
    return total