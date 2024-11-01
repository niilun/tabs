import logging, os

def get_file(path):
    with open(path) as f:
        return f.read()
    
def get_version():
    with open('version', 'r') as f:
        return f.read()

def get_all_units():
    # Find a better method for this (gets the absolute path of main.py and adds manually)
    with open(os.path.dirname(os.path.realpath(__name__)) + '/units/all_units.txt', 'r') as f:
        all_units = f.readline().split(', ')
    return all_units

def get_unit_eras():
    with open('unit_registry', 'r') as f:
        return f.readline().split(', ')