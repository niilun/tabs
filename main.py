from utilities.check_dependencies import check_dependencies
check_dependencies()

import logging, globals, configparser

from units import import_all_units

from game.mechanics.status_effects import status_effects
from game.game_window import display_main_window
from game.settings_window import reset_settings_file

from utilities.update_checker import update_check
from utilities.setup_logging import setup_logging

# Get config file. If not found, generate the default
config = configparser.ConfigParser()
config.optionxform = str

if not config.read('tabs.ini'):
    reset_settings_file()
    config.read('tabs.ini')

globals.loaded_config = config

version = config['Game']['Version']
repository_data = config['Network']['RepositoryData']
do_update = config.getboolean('Network', 'PerformUpdateCheck')
debug_level = config.getint('Debug', 'DebugLevel')

# Load logging and get session log file
log_path = setup_logging(debug_level)

def main():
    '''Starter main function'''
    logging.info(f'TABS Version {version}')
    logging.info(f'Development repository: https://github.com/{repository_data}')
    logging.info(f'Current session log @ {log_path}\n')

    # Check for updates
    if do_update:
        update_check(version, repository_data)
    else:
        logging.info('Skipping update check since PerformUpdateCheck is disabled.')
    import_all_units()

    effect_names = []
    for effect in status_effects:
        effect_names.append(effect.value[0])
    logging.debug(f'Loaded {len(status_effects)} status effects: {effect_names}')
    
    display_main_window()
    logging.shutdown()

if __name__ == '__main__':
    main()