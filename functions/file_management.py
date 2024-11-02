def get_file(path):
    '''
    Gets contents of a file path, absolute or relative.
    '''
    with open(path) as f:
        return f.read()
    
def get_version():
    '''
    Gets version number from the 'version' file.
    '''
    with open('version', 'r') as f:
        return f.read()