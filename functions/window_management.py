import logging
import tkinter as tk

unit_list_window_opened = False
unit_max_reached_window_opened = False
unbalanced_teams_window_opened = False

# Wrappers for game actions
def create_unit_ui_wrapper(selected_unit, team):
    from functions.unit_management import create_unit
    global main_window

    try:
        create_unit(selected_unit, team)
    # Create an info window saying unit was not found
    except Exception:
        not_found_window = tk.Toplevel(main_window)
        not_found_text = tk.Label(not_found_window, text=f'Unit {selected_unit} not found!').pack()
        not_found_close = tk.Button(not_found_window, text = 'Close', command=not_found_window.destroy).pack()
    
def take_next_action_ui_wrapper():
    from functions.unit_management import take_next_action
    global main_window

    try:
        take_next_action()
    except Exception:
        unbalanced_teams_window = tk.Toplevel(main_window)
        tk.Label(unbalanced_teams_window, text=f"Some teams don't have units! Add some before they can take their turns.").pack()
        tk.Button(unbalanced_teams_window, text = 'Close', command=unbalanced_teams_window.destroy).pack()

# UI
def display_unit_list():
    from functions.unit_management import get_all_units
    global main_window, unit_list_window_opened

    def close():
        global unit_list_window_opened

        unit_list_window_opened = False
        unit_help_window.destroy()
    
    if not unit_list_window_opened:
        unit_help_window = tk.Toplevel(main_window)

        tk.Label(unit_help_window, text=f'Available units: {", ".join(get_all_units())}').pack()
        tk.Button(unit_help_window, text = 'OK', command=close).pack()

        unit_list_window_opened = True

def display_unit_max_reached():
    global main_window, unit_max_reached_window_opened
    
    def close():
        global unit_max_reached_window_opened

        unit_max_reached_window_opened = False
        unit_max_window.destroy()
    
    if not unit_max_reached_window_opened:
        unit_max_window = tk.Toplevel(main_window)

        tk.Label(unit_max_window, text=f'The maximum number of units on the field at one time is 10!').pack()
        tk.Button(unit_max_window, text = 'OK', command=close).pack()

        unit_max_reached_window_opened = True


def display_main_window():
    '''Internal function'''
    from functions.file_management import get_version
    global unit_select_input, main_window

    # Left pane (unit select & info)
    main_window = tk.Tk()
    main_window.geometry('920x640')
    main_window.title('TABS')

    unit_select_input = tk.Entry()
    unit_select_input.pack()


    tk.Button(text = 'Summon (team 1)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(), 1)).pack()

    tk.Button(text = 'Summon (team 2)', command=lambda: create_unit_ui_wrapper(unit_select_input.get(), 2)).pack()

    tk.Button(text = 'Take next action', command=take_next_action_ui_wrapper).pack()

    tk.Button(text='Unit list', command=display_unit_list).pack()

    tk.Label(text = get_version()).pack()

    logging.debug('Running main window loop')
    main_window.mainloop()
    