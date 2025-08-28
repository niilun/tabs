import importlib, pkgutil, units, logging

unit_registry = {}

def import_all_units():
    '''Ran on startup, imports all units.'''

    imported_units = []
    for loader, module, pkg in pkgutil.iter_modules(units.__path__):
        # don't import the base unit as it is a model, not a real unit
        if module == 'base':
            continue
        imported_units.append(module)
        importlib.import_module(f'units.{module}')
    logging.debug(f'Imported units {imported_units}')

def register_new_unit(unit):
    '''Adds the unit to the registry the game uses. Necessary for it to be displayed in-game.'''
    unit_registry[unit().unit_name] = unit
    return unit