import tkinter as tk, globals, logging, configparser
from tkinter import messagebox

def display_settings_window(main_window):
    '''Shows the settings window.'''
    from .utilities import create_image_label

    # Load config
    loaded_config = configparser.ConfigParser()
    loaded_config.optionxform = str
    loaded_config.read('tabs.ini')

    # If the window already exists, reuse it. Otherwise, create it
    if globals.settings_window_active:
        settings_window = globals.settings_window_active
        for child in settings_window.winfo_children():
            child.destroy()
        settings_window.deiconify()
        settings_window.lift()
    else:
        settings_window = tk.Toplevel(main_window)
        settings_window.geometry('640x320')
        settings_window.title('TABS Settings')
        settings_window.resizable(False, False)
        # On close, save settings
        def close_window():
            settings_window.withdraw()
            save_config_file(loaded_config)

        settings_window.protocol('WM_DELETE_WINDOW', close_window)
        # Store it for later use
        globals.settings_window_active = settings_window
    
    # Display settings
    
    def save_setting(section, setting, entry):
        '''Saves a specific setting to the loaded config.'''
        loaded_config[section][setting] = entry.get()
        logging.debug(f'Setting section {section}, {setting} to {entry.get()}')

    for section in loaded_config.sections():
        section_label = tk.Label(settings_window, font = ('Arial', 12, 'bold'), text = section)
        section_label.pack(padx = 10, pady = 5, anchor = 'w')

        current_row = 0
        for setting, value in loaded_config[section].items():
            setting_frame = tk.Frame(settings_window)

            setting_label = tk.Label(setting_frame, text = setting, width = 20)
            setting_label.grid(row = current_row, column = 1, padx = 5)
            
            setting_box = tk.Entry(setting_frame)
            setting_box.insert(0, value)
            setting_box.grid(row = current_row, column = 2, padx = 5)
            
            save_button = tk.Button(setting_frame, text = 'Save', command = lambda sec = section, set = setting, box = setting_box: save_setting(sec, set, box))
            save_button.grid(row = current_row, column = 3, padx = 5)

            setting_frame.pack(anchor = 'w')
            current_row += 1

    # Reset settings & decoration
    config_icon = create_image_label(settings_window, 'assets/ui/settings_deco_64x.png')
    config_icon.place(x = 540, y = 30)

    config_reset = tk.Button(settings_window, text = 'Reset to default',command = reset_config_file_handler)
    config_reset.place(x = 500, y = 285)

def save_config_file(config):
    with open('tabs.ini', 'w+') as config_file:
        config_file.write('# Settings file for TABS\n\n')
        config_file.write('# Change this manually here, or\n')
        config_file.write('# you can use the in-game menu!\n\n')
        config.write(config_file)
    logging.info('Saved settings file.')

def reset_config_file():
    '''Resets the configuration file to default.'''
    config = configparser.ConfigParser()
    config = globals.default_config
    
    save_config_file(config)

def reset_config_file_handler():
    '''Handles calling reset_config_file() after a confirmation prompt.'''
    if messagebox.askquestion('TABS Settings', message = 'Are you sure you wish to reset ALL settings to default?'):
        reset_config_file()