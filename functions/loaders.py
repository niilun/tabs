import logging, tkinter as tk
from functions.unit_management import create_unit
from functions.file_management import get_version, get_all_units

def get_input_and_create_unit():
    global unit_select_input
    selected_unit = unit_select_input.get()
    try:
        create_unit(selected_unit)
    except Exception:
        print('Unit was not found!')

def display_unit_list():
    global main_window
    unit_help_window = tk.Toplevel(main_window)
    unit_help_text = tk.Label(unit_help_window, text=f'Available units: {", ".join(get_all_units())}')
    unit_help_close = tk.Button(unit_help_window, text = 'Close', command=unit_help_window.destroy)
    unit_help_text.pack()
    unit_help_close.pack()
    unit_help_window.mainloop()

def load_window():
    global unit_select_input, main_window
    main_window = tk.Tk()
    main_window.title('TAbS')
    unit_select_input = tk.Entry()
    unit_select_confirm = tk.Button(text = 'Summon unit', command=get_input_and_create_unit)
    unit_select_help = tk.Button(text='Unit list', command=display_unit_list)
    unit_select_input.pack()
    unit_select_confirm.pack()
    unit_select_help.pack()
    bottom_version_indicator = tk.Label(text = f'v{get_version()}')
    bottom_version_indicator.pack()
    logging.debug('Loaded main window')
    main_window.mainloop()
    