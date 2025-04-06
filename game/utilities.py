def create_image_label(master_window, path: str, zoomx: int = 1, zoomy: int = 1):
    '''Creates a tk Label containing an image, assigned to window master_window, with photo resource at path and zoom values zoomx and zoomy.'''
    import tkinter as tk

    created_image = tk.Label(master_window)
    created_image.img = tk.PhotoImage(file = path)
    created_image.img = created_image.img.zoom(zoomx, zoomy)
    created_image.configure(image = created_image.img)
    return created_image

def update_check(current_version, repository_data):
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
    '''Returns "True" if client_version is >= to the server_version, otherwise "False".'''

    # Versions (eg. 0.2.7) get converted to numbers like 27, which can be compared easily
    converted_client_version = client_version.replace('.', '').lstrip('0')
    converted_server_version = server_version.replace('.', '').lstrip('0')
    
    return converted_client_version >= converted_server_version