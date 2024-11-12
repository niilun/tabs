import logging
from functions.unit_management import all_units_map, all_eras_map
from functions.window_management import display_main_window

version = '0.2.0pre-2'

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

def main():
    '''Internal function'''
    logging.debug(f'TABS Version {version} | https://github.com/Leowondeh/TABS')

    logging.debug(f'Loaded units map with {len(all_units_map)} entries: {[unit.__name__ .replace("_", " ") for unit in all_units_map.values()]}')
    logging.debug(f'Loaded {len(all_eras_map)} eras')

    display_main_window()
    logging.shutdown()

if __name__ == '__main__':
    main()