from functions.file_management import get_all_units

def create_unit(unit):
    if unit not in get_all_units():
        raise Exception
    print(f'Unit {unit} found!')