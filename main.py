import logging
from functions.file_management import get_unit_eras
from functions.loaders import load_window
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s| %(message)s')

def main():
    for era in get_unit_eras():
        logging.debug(f'Loaded units from era {era}')
    
    load_window()

if __name__ == '__main__':
    main()