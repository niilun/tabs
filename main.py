import logging, requests, time, globals
from functions.unit_management import all_units_map
from functions.window_management import display_main_window
from functions.utilities import version_check
from other.status_effects import status_effects

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

def main():
    '''Internal function'''
    logging.info(f'TABS Version {globals.version}')
    logging.info(f'Report issues/suggest something at https://github.com/{globals.repository_id}')

    # Check for updates
    logging.info('Starting update check...')
    try:
        update_check = requests.get(f'https://api.github.com/repos/{globals.repository_id}/releases/latest') 
        server_version = update_check.json()['tag_name']
        if version_check(globals.version, server_version) == False:
            globals.update_available = True
            logging.warning('+-----------------------------------------------------------------------------------------+')
            logging.warning(f'| UPDATE FOUND! Download version {server_version} at https://github.com/{globals.repository_id}/releases/latest. |')
            logging.warning('+-----------------------------------------------------------------------------------------+')
    except Exception:
        logging.error('Error while checking for updates, skipping.')
    update_check.close()
    logging.info('Finished version check.')

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