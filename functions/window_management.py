import logging, sys
import tkinter as tk
from tkinter import messagebox

# Holder for battle info widgets
widgets_team_1 = []
widgets_team_2 = []

# Wrappers for game actions
def create_unit_ui_wrapper(selected_unit, team):
    '''Handler function to run create_unit()'''
    from functions.unit_management import create_unit
    global main_window  

    # Nudge the user instead of displaying an error message if input is empty
    invalid_inputs = ['', ' ', 'help']

    if selected_unit in invalid_inputs:
        display_unit_list()
        return

    try:
        create_unit(selected_unit, team)
    except Exception as error_message:
        messagebox.showerror('Error while creating unit', error_message)

def take_next_action_ui_wrapper():
    '''Handler function to run take_next_action()'''
    from functions.unit_management import take_next_action
    global main_window

    try:
        take_next_action()
    except Exception as error_message:
        messagebox.showerror('Error while taking next action', error_message)

def display_unit_list():
    '''Displays all loaded units in a generic info window.'''
    from functions.unit_management import all_units_map
    
    messagebox.showinfo('Unit list', f'Units available:\n{", ".join([unit.__name__.replace("_", " ") for unit in all_units_map.values()])}')

def update_scoreboard():
    '''Updates the scoreboard (battle info), checks for new units or death of already existing ones.'''
    from functions.unit_management import active_units_team_1, active_units_team_2
    
    for slot, unit in active_units_team_1.items():
        info_slot = widgets_team_1[slot - 1]
        if unit is None:
            info_slot['name'].config(text = 'Empty slot')
            info_slot['health'].delete('all')
            info_slot['health'].create_rectangle(0, 0, 60, 10, fill = 'red')
        else:
            unit_health_percent = unit.current_health / unit.max_health
            info_slot['name'].config(text=unit.unit_name)
            info_slot['health'].delete('all')

            info_slot['health'].create_rectangle(0, 0, 60 * unit_health_percent, 10, fill = 'green')
            info_slot['health'].create_rectangle(0, 60 * unit_health_percent, 0, 10, fill = 'red')
            if unit.armor > 0:
                unit_armor_percent = unit.armor / unit.max_health
                info_slot['health'].create_rectangle(0, 0, 60 * unit_armor_percent, 10, fill = 'yellow')

    for slot, unit in active_units_team_2.items():
        info_slot = widgets_team_2[slot - 1]
        if unit is None:
            info_slot['name'].config(text = 'Empty slot')
            info_slot['health'].delete('all')
            info_slot['health'].create_rectangle(0, 0, 60, 10, fill = 'red')
        else:
            unit_health_percent = unit.current_health / unit.max_health

            info_slot['name'].config(text=unit.unit_name)
            info_slot['health'].delete('all')
            info_slot['health'].create_rectangle(0, 0, 60 * unit_health_percent, 10, fill = 'green')
            info_slot['health'].create_rectangle(0, 60 * unit_health_percent, 0, 10, fill = 'red')
            if unit.armor > 0:
                unit_armor_percent = unit.armor / unit.max_health
                info_slot['health'].create_rectangle(0, 0, 60 * unit_armor_percent, 10, fill = 'yellow')

    logging.info('Updated battle scoreboard.')

def display_main_window():
    '''Main function to create the game tkinter window'''
    from main import version
    from .unit_management import all_units_map

    global unit_select_input, main_window

    main_window = tk.Tk()

    main_window.geometry('920x640')
    main_window.title('TABS')
    
    unit_select_frame = tk.Frame(main_window)

    unit_select_scrollbar = tk.Scrollbar(unit_select_frame)
    unit_select_input = tk.Listbox(unit_select_frame, yscrollcommand = unit_select_scrollbar.set)
    for unit in all_units_map.keys():
        unit_select_input.insert(tk.END, unit.title())
    
    unit_select_scrollbar.pack(side = 'right', fill = 'y')
    unit_select_scrollbar.config(command = unit_select_input.yview)
    unit_select_input.pack(side = 'left', fill = 'both', expand = True)

    unit_select_frame.pack(side = 'left', fill = 'y',anchor = 'nw', expand = True)

    # Summon buttons for both teams
    summon_buttons = tk.Frame(main_window)
    summon_buttons.pack()
    tk.Button(summon_buttons, text = 'Summon (team 1)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(unit_select_input.curselection()), 1)).grid(row = 0, column = 0)
    tk.Button(summon_buttons, text = 'Summon (team 2)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(unit_select_input.curselection()), 2)).grid(row = 0, column = 1)

    tk.Button(text = 'Take next action', command=take_next_action_ui_wrapper).pack()

    # Unit info bars
    battle_info = tk.Frame(main_window, pady = 20)
    battle_info.pack()

    # Create two rows of 5 frames linked to battle_info
    for i in range(2):
        for j in range(5):
            frame = tk.Frame(battle_info)

            # Use a placeholder file until an actual unit fills the slot
            unit_image = tk.Label(frame)
            unit_image.img = tk.PhotoImage(file='resources/units/placeholder.png')
            unit_image.config(image=unit_image.img)

            unit_health = tk.Canvas(frame, height = 10, width = 60, background = 'red')
            unit_name = tk.Label(frame, text = 'Empty slot')

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
    quit_button.place(relx = 0.19, rely = 1, x = 10, y = -20, anchor = 'w')
    
    settings_button = tk.Button(text = 'Settings')
    settings_button.place(relx = 0.26, rely = 1, x = 10, y = -20, anchor = 'w')

    unit_list_button = tk.Button(text = 'Unit list', command = display_unit_list)
    unit_list_button.place(relx = 0.359, rely = 1, x = 10, y = -20, anchor = 'w')

    version_indicator = tk.Label(text = f'v{version}')
    version_indicator.place(relx = 0.93, rely = 1, x = 10, y = -15, anchor = 'w')

    logging.info('Main window loaded.')
    main_window.mainloop()