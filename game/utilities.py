def setup_logging(log_level: int):
    import logging, sys, os, uuid, datetime

    # Create the 'logs' folder if it doesn't exist
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Set formatting (remove time from stdout to not clog console)
    stdout_format = logging.Formatter('%(levelname)s | %(message)s')
    file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setFormatter(stdout_format)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    current_uuid = uuid.uuid4()

    # Refresh uuid if it somehow already exists
    if os.path.exists(f'logs/{current_time} {current_uuid}.log'):
        current_uuid = uuid.uuid4()
    
    file_logger = logging.FileHandler(f'logs/{current_time} {current_uuid}.log')
    file_logger.setFormatter(file_format)

    logger.addHandler(stdout_logger)
    logger.addHandler(file_logger)

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

def clear_console():
    '''Clears the console.'''
    import os, platform
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')

def reload_game():
    '''Reloads the game by re-running python.'''
    import os, sys, logging
    # Flush file buffers so they are closed properly
    sys.stdout.flush()
    sys.stderr.flush()
    clear_console()
    logging.info(f'Reloading game, running {" ".join(sys.orig_argv)}')
    os.execl(sys.executable, *sys.orig_argv)

def show_error(title: str, message: str):
    from CTkMessagebox import CTkMessagebox
    CTkMessagebox(title = title, message = message, icon = 'assets/ui/exit_16x.png')

def show_info(title: str, message: str):
    from CTkMessagebox import CTkMessagebox
    CTkMessagebox(title = title, message = message, icon = 'assets/ui/info_16x.png')

def show_ask_question(title: str, question: str) -> bool:
    from CTkMessagebox import CTkMessagebox
    box = CTkMessagebox(title = title, message = question, icon = 'assets/ui/settings_64x.png', option_1 = 'Yes', option_2 = 'No')
    response = box.get()

    if response == 'Yes':
        return True
    return False
