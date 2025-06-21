def update_check(current_version, repository_data):
    '''Sends a request to a GitHub repo based on repository_data to check whether the current_version is >= compared to the GitHub version.'''
    import logging, globals, requests

    logging.info('Starting update check...')
    try:
        update_check = requests.get(f'https://api.github.com/repos/{repository_data}/releases/latest') 
        server_version = update_check.json()['tag_name']
        if version_check(current_version, server_version) == False:
            globals.update_available = True
            logging.warning('+-----------------------------------------------------------------------------------------+')
            logging.warning(f'| UPDATE FOUND! Download version {server_version} at https://github.com/{repository_data}/releases/latest. |')
            logging.warning('+-----------------------------------------------------------------------------------------+')
    except Exception:
        logging.error(f'Error while checking for updates, skipping.')
    logging.info('Finished version check.')

def version_check(client_version: str, server_version: str) -> bool:
    '''Returns "True" if client has a greater or equal version to server version, otherwise "False".'''
    from packaging.version import Version

    converted_client_version = Version(client_version)
    converted_server_version = Version(server_version)

    return converted_client_version >= converted_server_version