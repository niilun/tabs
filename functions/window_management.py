import logging
import tkinter as tk

def get_input_and_create_unit(selected_unit, team):
    from functions.unit_management import create_unit
    global main_window
    # try:
    create_unit(selected_unit, team)
    #     # Create an info window saying unit was not found
    #     not_found_window = tk.Toplevel(main_window)
    #     not_found_text = tk.Label(not_found_window, text=f'Unit {selected_unit} not found!').pack()
    #     not_found_close = tk.Button(not_found_window, text = 'Close', command=not_found_window.destroy).pack()

def display_unit_list():
    from functions.unit_management import get_all_units
    global main_window
    unit_help_window = tk.Toplevel(main_window)
    unit_help_window.title('TABS | Available units')

    tk.Label(unit_help_window, text=f'Available units: {", ".join(get_all_units())}').pack()
    tk.Button(unit_help_window, text = 'Close', command=unit_help_window.destroy).pack()

    unit_help_window.mainloop()

def display_unit_max_reached():
    global main_window
    unit_max_window = tk.Toplevel(main_window)
    unit_max_window.title('Max units reached!')
    tk.Label(unit_max_window, text=f'The maximum number of units on the field is 10!').pack()
    tk.Button(unit_max_window, text = 'Close', command=unit_max_window.destroy).pack()

    unit_max_window.mainloop()


def display_main_window():
    from functions.file_management import get_version
    global debug_enabled, unit_select_input, main_window

    # Left pane (unit select & info)
    main_window = tk.Tk()
    main_window.geometry('920x640')
    main_window.title('TABS')

    unit_select_input = tk.Entry()
    unit_select_input.pack()

    unit_select_confirm_1 = tk.Button(text = 'Summon unit (team 1)', command=lambda: get_input_and_create_unit(unit_select_input.get(), 1))
    unit_select_confirm_1.pack()

    unit_select_confirm_2 = tk.Button(text = 'Summon unit (team 2)', command=lambda: get_input_and_create_unit(unit_select_input.get(), 2))
    unit_select_confirm_2.pack()
    
    tk.Button(text='Unit list', command=display_unit_list).pack()

    tk.Label(text = get_version()).pack()

    logging.debug('Running main window loop')
    main_window.mainloop()
    