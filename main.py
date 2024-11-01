import logging
from functions.unit_management import get_unit_eras, get_all_units
from functions.window_management import display_main_window

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

def main():
    for era in get_unit_eras():
        logging.debug(f'Loaded units from era {era}')
    logging.debug(f'Available units: {", ".join(get_all_units())}')

    display_main_window()

if __name__ == '__main__':
    main()