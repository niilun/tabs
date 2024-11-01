import logging, os

def get_file(path):
    with open(path) as f:
        return f.read()
    
def get_version():
    with open('version', 'r') as f:
        return f.read()