import customtkinter as ctk, logging, globals
from PIL import Image
from .unit_management import all_units_map

def display_unit_stats(main_window, unit_select_input):
    '''Shows stats of selected unit in an info window.'''

    # Get the listbox selection
    try:
        selected_unit = unit_select_input.get(unit_select_input.curselection())
        selected_unit = all_units_map[selected_unit]()
    except Exception:
        # Tcl throws an error if there's no listbox selection, so we just return without clogging the console
        return
    
    # If the window already exists, reuse it. Otherwise, create it
    if globals.stat_window_active and globals.stat_window_active.winfo_exists():
        stat_window = globals.stat_window_active
        for child in stat_window.winfo_children():
            child.destroy()
        stat_window.deiconify()
        stat_window.lift()
    else:
        stat_window = ctk.CTkToplevel(main_window)
        stat_window.geometry('640x320')
        stat_window.resizable(False, False)
        stat_window.protocol('WM_DELETE_WINDOW', lambda: stat_window.withdraw())

        # Store it for later use
        globals.stat_window_active = stat_window

    stat_window.title(f'Unit info // {selected_unit.unit_name}')

    # Unit image
    unit_resource_path = f'assets/units/{selected_unit.unit_name.replace(" ", "-").lower()}.png'
    try:
        unit_image = ctk.CTkImage(light_image = Image.open(unit_resource_path), size = (128, 128))
        unit_image_label = ctk.CTkLabel(stat_window, text = '', image = unit_image)
    except Exception:
        logging.warning(f'Failed to find image {unit_resource_path}, using placeholder')
        unit_image = ctk.CTkImage(light_image = Image.open('assets/units/placeholder.png'), size = (128, 128))
        unit_image_label = ctk.CTkLabel(stat_window, text = '', image = unit_image)
    
    unit_image_label.pack(side = 'left', fill = 'y')

    # Line separator
    image_sep = ctk.CTkCanvas(stat_window, width = 2, height = 320)
    image_sep.create_rectangle(0, 0, 2, 320, fill = 'gray')
    image_sep.pack(side = 'left', fill = 'y')

    # Stats
    stat_frame = ctk.CTkFrame(stat_window)
    stat_frame.pack(side = 'left', anchor = 'n', padx = 10, pady = 10)
    
    health_icon = ctk.CTkImage(light_image = Image.open('assets/ui/health_16x.png'))
    health_icon_label = ctk.CTkLabel(stat_frame, text = '', image = health_icon)
    health_icon_label.grid(row = 0, column = 0)

    health_display = ctk.CTkLabel(stat_frame, text = f'{selected_unit.current_health} / {selected_unit.max_health} HP')
    health_display.grid(row = 0, column = 1)

    attack_icon = ctk.CTkImage(light_image = Image.open('assets/ui/attack_16x.png'))
    attack_icon_label = ctk.CTkLabel(stat_frame, text = '', image = attack_icon)
    attack_icon_label.grid(row = 1, column = 0)

    attack_display = ctk.CTkLabel(stat_frame, text = f'{selected_unit.attack_damage} Attack Damage')
    attack_display.grid(row = 1, column = 1)

    # Spacer & line break
    ctk.CTkLabel(stat_frame, text = '                \n').grid(row = 2, column = 0)

    # Abilities
    try:
        abilities = ', '.join(selected_unit.abilities)
    except AttributeError:
        abilities = 'Not defined in unit class!'

    abilities_icon = ctk.CTkImage(light_image = Image.open('assets/ui/abilities_16x.png'))
    abilities_icon_label = ctk.CTkLabel(stat_frame, text = '', image = abilities_icon)
    abilities_icon_label.grid(row = 3, column = 0)

    abilities_display = ctk.CTkLabel(stat_frame, text = f'Available abilities:')
    abilities_display.grid(row = 3, column = 1)
    abilities_list = ctk.CTkLabel(stat_frame, text = abilities)
    abilities_list.grid(row = 4, column = 1)

    logging.info(f'Showing unit info for {selected_unit.unit_name}')