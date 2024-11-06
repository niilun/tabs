import logging
from functions.unit_management import get_all_eras, get_all_units
from functions.window_management import display_main_window

version = '0.1.1dev'

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

def main():
    logging.debug(f'TABS Version {version} | https://github.com/Leowondeh/TABS')

    logging.debug(f'Loaded eras {(get_all_eras())}')
    logging.debug(f'Loaded units {(get_all_units())}')

    display_main_window()

if __name__ == '__main__':
    main()