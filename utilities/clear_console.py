def clear_console():
    '''Clears the console.'''
    import os, platform
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')