import logging, requests, globals, configparser

from game.unit_management import all_units_map
from game.mechanics.status_effects import status_effects

from game.game_window import display_main_window
from game.utilities import update_check
from game.settings_window import reset_config_file

# Get config file. If not found, generate the default
config = configparser.ConfigParser()

if config.read('tabs.ini') == []:
    reset_config_file()
config.read('tabs.ini')

globals.loaded_config = config
version = config['Game']['Version']
repository_data = config['Network']['RepositoryData']
do_update = config.getboolean('Network', 'PerformUpdateCheck')
debug_level = config.getint('Debug', 'DebugLevel')

logging.basicConfig(level = debug_level, format = '%(levelname)s | %(message)s')

def main():
    '''Internal function'''
    logging.info(f'TABS Version {version}')
    logging.info(f'Report issues/suggest something at https://github.com/{repository_data}')

    # Check for updates
    if do_update:
        update_check(version, repository_data)

    # Log loaded units/effects
    unit_names = []
    for unit in all_units_map.values():
        unit_names.append(unit().unit_name)
    logging.debug(f'Loaded units map with {len(all_units_map)} entries: {unit_names}')

    effect_names = []
    for effect in status_effects:
        effect_names.append(f'{effect.value[0]}')
    logging.debug(f'Loaded {len(status_effects)} status effects: {effect_names}')
    
    display_main_window()
    logging.shutdown()

if __name__ == '__main__':
    main()