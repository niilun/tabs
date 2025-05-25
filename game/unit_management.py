import logging

from units.warrior import warrior
from units.spearman import spearman
from units.man_at_arms import man_at_arms
from units.musketman import musketman
from units.line_infantry import line_infantry
from units.infantry import infantry
from units.mechanized_infantry import mechanized_infantry

# Maps units to their user-friendly name
all_units_map = {
    'Warrior': warrior,
    'Spearman': spearman,
    'Man-at-Arms': man_at_arms,
    'Musketman': musketman,
    'Infantry': infantry,
    'Line Infantry': line_infantry,
    'Mechanized Infantry': mechanized_infantry
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
    from game.game_window import update_scoreboard
    from globals import loaded_config

    if unit not in all_units_map:
        raise Exception('Unit does not exist or is not declared!')
    
    # Load scaling from settings
    health_scaling = loaded_config.getfloat('Game', 'UnitHealthScaling')
    attack_scaling = loaded_config.getfloat('Game', 'UnitAttackScaling')

    created_unit = all_units_map[unit]()
    
    # Apply scaling
    created_unit.current_health *= health_scaling
    created_unit.max_health *= health_scaling
    created_unit.attack_damage *= attack_scaling

    if team == 1:
        if get_total_active_units(1) >= 5:
            raise Exception('Team 1 is full!')
        
        logging.debug(f'Created unit {unit} in slot {find_first_available_slot(1)}.')
        active_units_team_1[find_first_available_slot(1)] = created_unit
    elif team == 2:
        if get_total_active_units(2) >= 5:
            raise Exception('Team 2 is full!')

        logging.debug(f'Created unit {unit} in slot {find_first_available_slot(2)} on team {team}.')
        active_units_team_2[find_first_available_slot(2)] = created_unit
    else:
        raise Exception(f"Invalid team call {team}")

    update_scoreboard()

def take_next_action():
    '''Calculates the next unit that's supposed to take its turn and runs its take_turn() method.'''
    global turn_counter
    turn_taken = False

    # No fights can happen between empty teams
    if get_total_active_units(1) == 0 or get_total_active_units(2) == 0:
        raise Exception('No fights can happen between empty teams! \nAdd some units to both before continuing to take turns.')
    
    # Reset to a new turn cycle if all turns exhausted
    if turn_counter > get_total_active_units(1) + get_total_active_units(2):
        turn_counter = 1
    
    if turn_counter <= get_total_active_units(1) and not turn_taken:
        logging.debug(f'Next turn: team 1, slot {turn_counter}.')
        try:
            unit = active_units_team_1.get(turn_counter)
            if unit:
                unit.take_turn(active_units_team_2)
            else:
                turn_counter += 1
                logging.debug('Skipping turn because of missing unit.')
                take_next_action()
        except Exception as e:
            logging.error(f'Error when taking unit turn: {e}!')
            turn_counter += 1

        turn_counter += 1
        turn_taken = True

    if turn_counter <= get_total_active_units(1) + get_total_active_units(2) and not turn_taken:
        logging.debug(f'Next turn: team 2, slot {turn_counter - get_total_active_units(1)}.')
        try:
            unit = active_units_team_2.get(turn_counter - get_total_active_units(1))
            if unit:
                unit.take_turn(active_units_team_1)
            else:
                turn_counter += 1
                logging.debug('Skipping turn because of missing unit.')
                take_next_action()
        except Exception as e:
            logging.error(f'Error when taking unit turn: {e}!')
            turn_counter += 1

        turn_counter += 1
        turn_taken = True

    cleanup_units()

def cleanup_units():
    '''Checks for dead units in both teams and removes them from the game'''
    from game.game_window import update_scoreboard
    
    # Use copies when iterating
    counter = 1
    for unit in active_units_team_1.copy().values():
        if unit == None:
            pass
        elif unit.current_health <= 0:
            logging.info(f'Unit {unit.unit_name} in slot {counter} in team 1 dead, removing.')
            active_units_team_1[counter] = None
        counter += 1

    counter = 1
    for unit in active_units_team_2.copy().values():
        if unit == None:
            pass
        elif unit.current_health <= 0:
            logging.info(f'Unit {unit.unit_name} in slot {counter} in team 2 dead, removing.')
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
        raise Exception(f'Invalid team call {team} in {__name__}!')

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
        raise Exception(f'Invalid team call {team} in {__name__}!')
    return total