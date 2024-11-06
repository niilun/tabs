def get_file(path):
    '''
    Gets contents of a file path, absolute or relative.
    '''
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise Exception('File does not exist')