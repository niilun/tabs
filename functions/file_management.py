def get_file(path):
    '''
    Gets contents of a file path, absolute or relative.
    '''
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise Exception('File does not exist')
    
def get_version():
    '''
    Gets version number from the 'version' file.
    '''
    try:
        with open('version', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return 'v<missingNo>'