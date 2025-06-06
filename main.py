import pkg_resources, sys, subprocess

requirements = {'pyinstaller', 'requests', 'configparser', 'customtkinter', 'ctklistbox', 'ctkmessagebox'}
found = {pkg.key for pkg in pkg_resources.working_set}
missing = requirements - found

if missing:
    print(f'Found missing packages: {", ".join(missing)}')
    print('Installing them... Please wait.')
    python_path = sys.executable
    try:
        subprocess.check_call([python_path, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    except Exception:
        print('Failed to install dependencies. Try running "pip install -r requirements.txt" from your terminal while in the TABS root folder.')

import logging, globals, configparser

from game.unit_management import all_units_map
from game.mechanics.status_effects import status_effects

from game.game_window import display_main_window
from game.utilities import update_check, setup_logging
from game.settings_window import reset_settings_file

# Get config file. If not found, generate the default
config = configparser.ConfigParser()

if config.read('tabs.ini') == []:
    reset_settings_file()
config.read('tabs.ini')

globals.loaded_config = config
version = config['Game']['Version']
repository_data = config['Network']['RepositoryData']
do_update = config.getboolean('Network', 'PerformUpdateCheck')
debug_level = config.getint('Debug', 'DebugLevel')

# Load logging
setup_logging(debug_level)

def main():
    '''Starter main function'''
    logging.info(f'TABS Version {version}')
    logging.info(f'Development repository: https://github.com/{repository_data}\n')

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