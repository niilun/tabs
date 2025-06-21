import importlib, pkgutil, units, logging

unit_registry = {}

def import_all_units():
    '''Ran on startup, imports all units.'''

    for loader, module, pkg in pkgutil.iter_modules(units.__path__):
        if module == 'base':
            continue
        logging.debug(f'Imported unit {module}')
        importlib.import_module(f'units.{module}')

def register_new_unit(unit):
    '''Adds the unit to the registry the game uses. Necessary for it to be displayed in-game.'''
    unit_registry[unit().unit_name] = unit
    return unit