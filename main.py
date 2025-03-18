import logging
from functions.unit_management import all_units_map, all_eras_map
from constants import status_effects
from functions.window_management import display_main_window

version = f'0.4.0'

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

def main():
    '''Internal function'''
    logging.debug(f'TABS Version {version} | https://github.com/Leowondeh/TABS')

    # get unit/era/status effect names and make them readable in console
    unit_names = []
    for unit in all_units_map.values():
        unit_names.append(unit.__name__.replace('_', ' '))
    logging.debug(f'Loaded units map with {len(all_units_map)} entries: {unit_names}')

    era_names = []
    for era in all_eras_map.keys():
        era_names.append(era.replace('_', ' '))
    logging.debug(f'Loaded era map with {len(all_eras_map)} entries: {era_names}')

    effect_names = ''
    for effect in status_effects:
        effect_names += f'{effect.value[0]}, '
    logging.debug(f'Loaded {len(status_effects)} status effects: {effect_names[:-2]}')
    
    display_main_window()
    logging.shutdown()

if __name__ == '__main__':
    main()