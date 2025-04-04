def get_file(path):
    '''
    Gets contents of a file path, absolute or relative.
    '''
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise Exception('File does not exist')
    
def create_image_label(master_window, path: str, zoomx: int = 1, zoomy: int = 1):
    import tkinter as tk

    created_image = tk.Label(master_window)
    created_image.img = tk.PhotoImage(file = path)
    created_image.img = created_image.img.zoom(zoomx, zoomy)
    created_image.configure(image = created_image.img)
    return created_image
    
def version_check(client_version: str, server_version: str) -> bool:
    '''Returns "True" if client_version is >= to the server_version, otherwise "False".'''

    # Versions (eg. 0.2.7) get converted to numbers like 27, which can be compared easily
    converted_client_version = client_version.replace('.', '').lstrip('0')
    converted_server_version = server_version.replace('.', '').lstrip('0')
    
    return converted_client_version >= converted_server_version