import logging, os

from functions.window_management import display_unit_max_reached

from units.ancient import *
from units.classical import *

# Current number of units active
max_id = 0
active_units_team_1 = []
active_units_team_2 = []

def create_unit(unit, team):
    global max_id
    if unit not in get_all_units():
        raise Exception
    
    if max_id >= 10:
        display_unit_max_reached()
        return
    
    max_id = max_id + 1

    if unit == 'warrior':
        created_unit = Warrior(max_id)
    elif unit == 'spearman':
        created_unit = Spearman(max_id)
    
    if team == 1:
        
        active_units_team_1.append(created_unit)
    else:
        active_units_team_2.append(created_unit)
    
    logging.debug(f'Created unit {unit} ID {max_id}')
    logging.debug(f'''New unit lists:
                      Team 1: {active_units_team_1}
                      Team 2: {active_units_team_2}''')

def get_all_units():
    # Find a better method for this (gets the absolute path of main.py and adds manually)
    with open(os.path.dirname(os.path.realpath(__name__)) + '/units_list', 'r') as f:
        all_units = f.readline().split(', ')
    return all_units

def get_unit_eras():
    with open('eras_list', 'r') as f:
        return f.readline().split(', ')