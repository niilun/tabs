import logging, sys
import tkinter as tk
from tkinter import messagebox
from .utilities import create_image_label

# Holder for battle info widgets
widgets_team_1 = []
widgets_team_2 = []

# Wrappers for game actions
def create_unit_ui_wrapper(team):
    '''Handler function to run create_unit()'''
    from functions.unit_management import create_unit
    global main_window, unit_select_input
    try:
        selected_unit = unit_select_input.get(unit_select_input.curselection())
    except Exception:
        # Tcl throws an error if there's no listbox selection, so we just return without clogging the console
        return
    
    try:
        create_unit(selected_unit, team)
    except Exception as error_message:
        messagebox.showerror('Error while creating unit', error_message)

def take_next_action_ui_wrapper():
    '''Handler function to run take_next_action()'''
    from functions.unit_management import take_next_action

    try:
        take_next_action()
    except Exception as error_message:
        messagebox.showerror('Error while taking next action', error_message)

def display_unit_list():
    '''Displays all loaded units in a generic info window.'''
    from functions.unit_management import all_units_map
    
    messagebox.showinfo('Unit list', f'Units available:\n{", ".join([unit.__name__.replace("_", " ") for unit in all_units_map.values()])}')

def display_unit_stats():
    '''Shows stats of selected unit in an info window.'''
    from .unit_management import all_units_map
    import globals
    global main_window, unit_select_input

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
    try:
        unit_image = create_image_label(stat_window, f'resources/units/{selected_unit.unit_name.replace(" ", "-").lower()}.png', 2, 2)
    except Exception:
        logging.warning(f'Failed to find image resources/units/{selected_unit.unit_name.replace(" ", "-").lower()}.png, using placeholder')
        unit_image = create_image_label(stat_window, f'resources/units/placeholder.png', 2, 2)
    
    unit_image.pack(side = 'left', fill = 'y')

    # Line separator
    image_sep = tk.Canvas(stat_window, width = 2, height = 320)
    image_sep.create_rectangle(0, 0, 2, 320, fill = 'gray')
    image_sep.pack(side = 'left', fill = 'y')
    
    # Stats
    stat_frame = tk.Frame(stat_window)
    stat_frame.pack(side = 'left', anchor = 'n', padx = 10, pady = 10)

    health_icon = create_image_label(stat_frame, 'resources/ui/health.png')
    health_icon.grid(row = 0, column = 0)
    health_display = tk.Label(stat_frame, text = f'{selected_unit.current_health} / {selected_unit.max_health} HP')
    health_display.grid(row = 0, column = 1)

    attack_icon = create_image_label(stat_frame, 'resources/ui/attack.png')
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

    abilities_icon = create_image_label(stat_frame, 'resources/ui/abilities.png')
    abilities_icon.grid(row = 3, column = 0)
    abilities_display = tk.Label(stat_frame, text = f'Available abilities:')
    abilities_display.grid(row = 3, column = 1)
    abilities_list = tk.Label(stat_frame, text = abilities)
    abilities_list.grid(row = 4, column = 1)

def update_scoreboard():
    '''Updates the scoreboard (battle info), checks for new units or the death of existing ones.'''
    from functions.unit_management import active_units_team_1, active_units_team_2
    # Function that resets the given slot to default (called if a unit dies)
    def set_default_slot(slot):
        try:
            slot['name'].config(text = 'Empty slot')
            slot['health'].delete('all')
            slot['health'].create_rectangle(0, 0, 80, 20, fill = 'gray')
        except Exception:
            raise Exception(f'Invalid slot call {slot} in {__name__}')

    for slot, unit in active_units_team_1.items():
        info_slot = widgets_team_1[slot - 1]
        
        if unit is None:
            # If unit doesn't exist, set the slot back to default
            set_default_slot(info_slot)
        else:
            unit_health_percent = unit.current_health / unit.max_health

            # If name is too long add dots so widgets don't move (TODO: find a way around this)
            if len(unit.unit_name) > 11:
                info_slot['name'].config(text=f'{unit.unit_name[:11].strip()}...')
            else:
                info_slot['name'].config(text=unit.unit_name)
            info_slot['health'].delete('all')

            info_slot['health'].create_rectangle(0, 0, 80 * unit_health_percent, 20, fill = 'green')
            info_slot['health'].create_rectangle(80 * unit_health_percent, 0, 80, 20, fill = 'red')
            if unit.armor > 0:
                unit_armor_percent = unit.armor / unit.max_health
                info_slot['health'].create_rectangle(0, 0, 80 * unit_armor_percent, 20, fill = 'yellow')

    for slot, unit in active_units_team_2.items():
        info_slot = widgets_team_2[slot - 1]

        if unit is None:
            # If unit doesn't exist, set the slot back to default
            set_default_slot(info_slot)
        else:
            unit_health_percent = unit.current_health / unit.max_health

            # If name is too long add dots so widgets don't move (TODO: find a way around this)
            if len(unit.unit_name) > 11:
                info_slot['name'].config(text=f'{unit.unit_name[:11].strip()}...')
            else:
                info_slot['name'].config(text=unit.unit_name)
            info_slot['health'].delete('all')
            info_slot['health'].create_rectangle(0, 0, 80 * unit_health_percent, 20, fill = 'green')
            info_slot['health'].create_rectangle(80 * unit_health_percent, 0, 80, 20, fill = 'red')
            if unit.armor > 0:
                unit_armor_percent = unit.armor / unit.max_health
                info_slot['health'].create_rectangle(0, 0, 80 * unit_armor_percent, 20, fill = 'yellow')

    logging.info('Updated battle scoreboard.')

def display_settings_window():
    logging.info('Settings are not implemented yet!')

def display_main_window():
    '''Main function to create the game tkinter window'''
    from .unit_management import all_units_map
    import globals

    global unit_select_input, main_window

    main_window = tk.Tk()
    main_window.title('TABS')

    if globals.update_available:
        main_window.title('TABS | update available, check console!') 
    
    main_window.geometry('920x640')
    main_window.resizable(False, False)
    unit_select_frame = tk.Frame(main_window)

    unit_select_scrollbar = tk.Scrollbar(unit_select_frame)
    unit_select_input = tk.Listbox(unit_select_frame, yscrollcommand = unit_select_scrollbar.set)
    for unit in all_units_map.keys():
        unit_select_input.insert(tk.END, unit)
    
    unit_select_scrollbar.pack(side = 'right', fill = 'y')
    unit_select_scrollbar.config(command = unit_select_input.yview)
    unit_select_input.pack(side = 'left', fill = 'both', expand = True)

    unit_select_frame.pack(side = 'left', fill = 'y',anchor = 'nw', expand = True)

    # Summon buttons for both teams
    tk.Button(text = 'Summon', command=lambda: create_unit_ui_wrapper(1)).place(x = 195, y = 220)
    tk.Button(text = 'Summon', command=lambda: create_unit_ui_wrapper(2)).place(x = 195, y = 383)

    tk.Button(text = 'Take next action', command=take_next_action_ui_wrapper).place(x = 530, y = 80)

    # Unit info bars
    battle_info = tk.Frame(main_window, pady=20)
    battle_info.place(relx=0.32, y=120)

    # Create two rows of 5 frames linked to battle_info
    for i in range(2):
        for j in range(5):
            frame = tk.Frame(battle_info)

            # Use a placeholder file until an actual unit fills the slot
            unit_image = tk.Label(frame)
            unit_image.img = tk.PhotoImage(file='resources/units/placeholder.png')
            unit_image.img = unit_image.img.zoom(2, 2)
            unit_image.config(image=unit_image.img)

            unit_health = tk.Canvas(frame, height=15, width=80, background='gray')
            unit_name = tk.Label(frame, text='Empty slot', font=("TkDefaultFont", 12))

            unit_image.pack()
            unit_name.pack()
            unit_health.pack()

            widget_dict = {
                'image': unit_image,
                'name': unit_name,
                'health': unit_health
            }

            if i == 0:
                widgets_team_1.append(widget_dict)
            elif i == 1:
                widgets_team_2.append(widget_dict)

            frame.grid(row=i, column=j)

    # Utilities
    quit_button = tk.Button(text='Quit', command=sys.exit)
    quit_button.place(x = 180, rely = 1, y = -20, anchor = 'w')
    
    settings_button = tk.Button(text = 'Settings', command = display_settings_window)
    settings_button.place(x = 236, rely = 1, y = -20, anchor = 'w')

    unit_list_button = tk.Button(text = 'Unit info', command = display_unit_stats)
    unit_list_button.place(x = 318, rely = 1, y = -20, anchor = 'w')

    version_indicator = tk.Label(text = f'v{globals.version}')
    version_indicator.place(relx = 0.94, rely = 1, y = -15, anchor = 'w')

    logging.info('Main window loaded.')
    main_window.mainloop()