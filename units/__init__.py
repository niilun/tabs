import sys, os, importlib.util, logging

unit_registry = {}

# dev_modules is a blacklist for units that either shouldn't be imported (like base units) or helper units (like minions)
dev_modules = {'base', '__init__'}

def import_all_units():
    '''Ran on startup, imports all units.'''
    imported_units = []

    # if system packages are frozen, add that to the directory path
    if hasattr(sys, '_MEIPASS'):
        units_dir = os.path.join(sys._MEIPASS, 'units')
    else:
        units_dir = os.path.dirname(__file__)

    for file in os.listdir(units_dir):
        if file.endswith('.py') and file[:-3] not in dev_modules:
            module_name = file[:-3]
            module_spec = importlib.util.spec_from_file_location(f'units.{module_name}', os.path.join(units_dir, file))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            imported_units.append(module_name)
    logging.debug(f'Imported units {imported_units}')

def register_new_unit(unit):
    '''Adds the unit to the registry the game uses. Necessary for it to be displayed in-game.'''
    unit_registry[unit().unit_name] = unit
    return unit