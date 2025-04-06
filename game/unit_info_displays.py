import tkinter as tk, logging, globals
from tkinter import messagebox

from .unit_management import all_units_map
from .utilities import create_image_label

def display_unit_stats(main_window, unit_select_input):
    '''Shows stats of selected unit in an info window.'''

    # Get the listbox selection
    try:
        selected_unit = unit_select_input.get(unit_select_input.curselection())
    except Exception:
        # Tcl throws an error if there's no listbox selection, so we just return without clogging the console
        return
    
    # If the window already exists, reuse it. Otherwise, create it
    if globals.stat_window_active:
        stat_window = globals.stat_window_active
        for child in stat_window.winfo_children():
            child.destroy()
        stat_window.deiconify()
        stat_window.lift()
    else:
        stat_window = tk.Toplevel(main_window)
        stat_window.geometry('640x320')
        stat_window.resizable(False, False)
        stat_window.protocol('WM_DELETE_WINDOW', lambda: stat_window.withdraw())
        # Store it for later use
        globals.stat_window_active = stat_window
    
    selected_unit = all_units_map[selected_unit]()
    stat_window.title(f'Unit info for {selected_unit.unit_name}')

    # Unit image
    unit_resource_path = f'assets/units/{selected_unit.unit_name.replace(" ", "-").lower()}.png'
    try:
        unit_image = create_image_label(stat_window, unit_resource_path, 2, 2)
    except Exception:
        logging.warning(f'Failed to find image {unit_resource_path}, using placeholder')
        unit_image = create_image_label(stat_window, f'assets/units/placeholder.png', 2, 2)
    
    unit_image.pack(side = 'left', fill = 'y')

    # Line separator
    image_sep = tk.Canvas(stat_window, width = 2, height = 320)
    image_sep.create_rectangle(0, 0, 2, 320, fill = 'gray')
    image_sep.pack(side = 'left', fill = 'y')
    
    # Stats
    stat_frame = tk.Frame(stat_window)
    stat_frame.pack(side = 'left', anchor = 'n', padx = 10, pady = 10)

    health_icon = create_image_label(stat_frame, 'assets/ui/health_16x.png')
    health_icon.grid(row = 0, column = 0)
    health_display = tk.Label(stat_frame, text = f'{selected_unit.current_health} / {selected_unit.max_health} HP')
    health_display.grid(row = 0, column = 1)

    attack_icon = create_image_label(stat_frame, 'assets/ui/attack_16x.png')
    attack_icon.grid(row = 1, column = 0)
    attack_display = tk.Label(stat_frame, text = f'{selected_unit.attack_damage} Attack Damage')
    attack_display.grid(row = 1, column = 1)

    # Spacer & line break
    tk.Label(stat_frame, text = '                \n').grid(row = 2, column = 0)

    # Abilities
    try:
        abilities = ', '.join(selected_unit.abilities)
    except AttributeError:
        abilities = 'not defined in unit class'

    abilities_icon = create_image_label(stat_frame, 'assets/ui/abilities_16x.png')
    abilities_icon.grid(row = 3, column = 0)
    abilities_display = tk.Label(stat_frame, text = f'Available abilities:')
    abilities_display.grid(row = 3, column = 1)
    abilities_list = tk.Label(stat_frame, text = abilities)
    abilities_list.grid(row = 4, column = 1)
    logging.info(f'Showing unit info for {selected_unit.unit_name}')

def display_unit_list():
    '''Displays all loaded units in a generic info window.'''
    from game.unit_management import all_units_map
    
    messagebox.showinfo('Unit list', f'Units available:\n{", ".join([unit.__name__.replace("_", " ") for unit in all_units_map.values()])}')