import logging
import tkinter as tk

# Variables to prevent duplicate windows
unit_list_window_opened = False
any_error_window_opened = False

# Wrappers for game actions
def create_unit_ui_wrapper(selected_unit, team):
    '''Internal function'''
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
    '''Internal function'''
    from functions.unit_management import take_next_action
    global main_window

    try:
        take_next_action()
    except Exception as error_message:
        display_error_window(f'Error when taking next action: \n{error_message}')

# UI
def display_error_window(error_message):
        '''
        Displays a standard error window with message error_message.
        '''
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
    '''Internal function'''
    from main import version

    global unit_select_input, main_window

    main_window = tk.Tk()

    main_window.geometry('920x640')
    main_window.title('TABS')

    # Left pane (unit select & info)
    # left_pane = tk.Frame(main_window)
    unit_select_input = tk.Entry()
    unit_select_input.pack()

    tk.Button(text = 'Summon (team 1)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(), 1)).pack()

    tk.Button(text = 'Summon (team 2)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(), 2)).pack()

    tk.Button(text = 'Take next action', command=take_next_action_ui_wrapper).pack()

    tk.Button(text='Unit list', command=display_unit_list).pack()

    tk.Label(text = f'v{version}').pack()

    logging.debug('Running main window loop')
    main_window.mainloop()
    