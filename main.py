import logging
from functions.unit_management import all_units_map, all_eras_map
from functions.window_management import display_main_window

version = '0.2.0pre-2'

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

def main():
    '''Internal function'''
    logging.debug(f'TABS Version {version} | https://github.com/Leowondeh/TABS')

    # Get unit names and make them readable in console
    unit_names = []
    for unit in all_units_map.values():
        unit_names.append(unit.__name__.replace('_', ' '))
    logging.debug(f'Loaded units map with {len(all_units_map)} entries: {unit_names}')

    # Same with era names
    era_names = []
    for era in all_eras_map.keys():
        era_names.append(era.replace('_', ' '))
    logging.debug(f'Loaded era map with {len(all_eras_map)} entries: {era_names}')

    display_main_window()
 
    # Called once the window loop (everything) shuts down
    logging.shutdown()

if __name__ == '__main__':
    main()