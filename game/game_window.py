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
    from game.unit_management import create_unit
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
    from game.unit_management import take_next_action

    try:
        take_next_action()
    except Exception as error_message:
        messagebox.showerror('Error while taking next action', error_message)

def update_scoreboard():
    '''Updates the scoreboard (battle info), checks for new units or the death of existing ones.'''
    from game.unit_management import active_units_team_1, active_units_team_2
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

def display_main_window():
    '''Main function to create the game tkinter window'''
    from .unit_management import all_units_map
    from .unit_info_displays import display_unit_stats
    from .settings_window import display_settings_window
    import globals, configparser

    global unit_select_input, main_window

    config = configparser.ConfigParser()
    config.read('tabs.ini')
    version = config['Game']['Version']

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
    tk.Button(text = 'Summon', command = lambda: create_unit_ui_wrapper(1)).place(x = 190, y = 220)
    tk.Button(text = 'Summon', command = lambda: create_unit_ui_wrapper(2)).place(x = 190, y = 383)

    take_next_action_button = tk.Button(text = 'Take next action', compound = 'left', command = take_next_action_ui_wrapper)
    take_next_action_button.img = tk.PhotoImage(file = 'assets/ui/next_16x.png')
    take_next_action_button.configure(image = take_next_action_button.img)
    take_next_action_button.place(x = 510, y = 80)

    # Unit info bars
    battle_info = tk.Frame(main_window, pady=20)
    battle_info.place(relx=0.30, y=120)

    # Create two rows of 5 frames linked to battle_info
    for i in range(2):
        for j in range(5):
            frame = tk.Frame(battle_info)

            # Use a placeholder file until an actual unit fills the slot
            unit_image = tk.Label(frame)
            unit_image.img = tk.PhotoImage(file = 'assets/units/placeholder.png')
            unit_image.img = unit_image.img.zoom(2, 2)
            unit_image.config(image = unit_image.img)

            unit_health = tk.Canvas(frame, height = 15, width = 80, background = 'gray')
            unit_name = tk.Label(frame, text = 'Empty slot', font = ("TkDefaultFont", 12))

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
    quit_button = tk.Button(text = 'Quit', compound = 'left', command = sys.exit)
    quit_button.img = tk.PhotoImage(file = 'assets/ui/exit_16x.png')
    quit_button.configure(image = quit_button.img)
    quit_button.place(x = 180, rely = 1, y = -20, anchor = 'w')
    
    settings_button = tk.Button(text = 'Settings', compound = 'left', command = lambda: display_settings_window(main_window))
    settings_button.img = tk.PhotoImage(file = 'assets/ui/settings_16x.png')
    settings_button.configure(image = settings_button.img)
    settings_button.place(x = 265, rely = 1, y = -20, anchor = 'w')

    unit_info_button = tk.Button(text = 'Unit info', compound = 'left', command = lambda: display_unit_stats(main_window, unit_select_input))
    unit_info_button.img = tk.PhotoImage(file = 'assets/ui/info_16x.png')
    unit_info_button.configure(image = unit_info_button.img)
    unit_info_button.place(x = 375, rely = 1, y = -20, anchor = 'w')

    version_indicator = tk.Label(text = f'v{version}')
    version_indicator.place(relx = 0.94, rely = 1, y = -15, anchor = 'w')

    logging.info('Main window loaded.')
    main_window.mainloop()