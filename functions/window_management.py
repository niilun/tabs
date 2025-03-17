import logging
import tkinter as tk

# Variables to prevent duplicate windows
unit_list_window_opened = False
any_error_window_opened = False

# Holder for battle info widgets
widgets_team_1 = []
widgets_team_2 = []

# Wrappers for game actions
def create_unit_ui_wrapper(selected_unit, team):
    '''Handler function to run create_unit()'''
    from functions.unit_management import create_unit
    global main_window  

    invalid_inputs = ['', ' ', 'help']

    if selected_unit in invalid_inputs:
        display_unit_list()
        return

    try:
        create_unit(selected_unit, team)
    except Exception as error_message:
        display_error_window(f'Error when creating unit: \n{error_message}')
    
def take_next_action_ui_wrapper():
    '''Handler function to run take_next_action()'''
    from functions.unit_management import take_next_action
    global main_window

    try:
        take_next_action()
    except Exception as error_message:
        display_error_window(f'Error when taking next action: \n{error_message}')

# UI
def display_error_window(error_message):
    '''Displays a standard error window with message error_message.'''
    global main_window, any_error_window_opened

    def close():
        global any_error_window_opened

        any_error_window_opened = False
        error_window.destroy()

    if not any_error_window_opened:
        error_window = tk.Toplevel(main_window)
        tk.Label(error_window, text=f"{error_message}").pack()
        tk.Button(error_window, text = 'Close', command=close).pack()

def display_unit_list():
    '''Displays all loaded units in a generic info window.'''
    from functions.unit_management import all_units_map
    global main_window, unit_list_window_opened

    def close():
        global unit_list_window_opened

        unit_list_window_opened = False
        unit_help_window.destroy()
    
    if not unit_list_window_opened:
        unit_help_window = tk.Toplevel(main_window)

        tk.Label(unit_help_window, text=f'Available units: {", ".join([unit.__name__.replace("_", " ") for unit in all_units_map.values()])}').pack()
        tk.Button(unit_help_window, text = 'OK', command=close).pack()

        unit_list_window_opened = True

def display_main_window():
    '''Main function to create the game tkinter window'''
    from main import version

    global unit_select_input, main_window

    main_window = tk.Tk()

    main_window.geometry('920x640')
    main_window.title('TABS')

    unit_select_input = tk.Entry()
    unit_select_input.pack()

    tk.Button(text = 'Summon (team 1)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(), 1)).pack()
    tk.Button(text = 'Summon (team 2)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(), 2)).pack()

    tk.Button(text = 'Take next action', command=take_next_action_ui_wrapper).pack()

    tk.Button(text='Unit list', command=display_unit_list).pack()

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

            unit_health = tk.Label(frame, text='100/100')
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

    # Quit button and version indicator
    tk.Button(text='Quit', command=quit).pack()
    tk.Label(text = f'v{version}').pack(side = tk.BOTTOM)

    logging.debug('Running main window loop')
    main_window.mainloop()