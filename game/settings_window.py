import customtkinter as ctk, globals, logging, configparser
from .utilities import show_ask_question

setting_references = {}

def display_settings_window(main_window):
    '''Shows the settings window.'''
    from PIL import Image

    # Load settings
    loaded_settings = configparser.ConfigParser()
    loaded_settings.optionxform = str
    loaded_settings.read('tabs.ini')

    # If the window already exists and is valid, reuse it. Otherwise, create it
    if globals.settings_window_active and globals.settings_window_active.winfo_exists():
        settings_window = globals.settings_window_active
        for child in settings_window.winfo_children():
            child.destroy()
        settings_window.deiconify()
        settings_window.lift()
    else:
        settings_window = ctk.CTkToplevel(main_window)
        settings_window.geometry('640x320')
        settings_window.title('TABS Settings')
        settings_window.resizable(False, False)

        # Store it for later use
        globals.settings_window_active = settings_window

    # Display settings

    row = 0
    for section in loaded_settings.sections():
        section_label = ctk.CTkLabel(settings_window, font = ('Arial', 12, 'bold'), text = section)
        section_label.grid(row = row, column = 0, padx = 10, pady = (2, 2), sticky = 'w')
        row += 1

        for setting, value in loaded_settings[section].items():
            setting_frame = ctk.CTkFrame(settings_window)
            setting_frame.grid(row = row, column = 0, padx = 10, pady = 2, sticky = 'w')

            setting_label = ctk.CTkLabel(setting_frame, text = setting, width = 120, anchor = 'w')
            setting_label.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = 'w')

            setting_box = ctk.CTkEntry(setting_frame, width = 180)
            setting_box.insert(0, value)
            setting_box.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = 'w')
            
            setting_references[(section, setting)] = setting_box

            row += 1

    # Reset settings & decoration
    settings_image = ctk.CTkImage(light_image = Image.open('assets/ui/settings_deco_64x.png'), size = (64, 64))
    settings_icon = ctk.CTkLabel(settings_window, text = '', image = settings_image)
    settings_icon.place(x = 530, y = 30)

    settings_disclaimer = ctk.CTkLabel(settings_window, text='Settings only apply\nafter game restart!')
    settings_disclaimer.place(x = 500, y = 110)

    save_button = ctk.CTkButton(settings_window, text = 'Save', width = 60, command = lambda: get_and_save_settings(loaded_settings))
    save_button.place(x = 570, y = 250)

    settings_reset = ctk.CTkButton(settings_window, text = 'Reset to default', width = 120, command = lambda: reset_settings_file_handler())
    settings_reset.place(x = 510, y = 285)

def get_and_save_settings(settings):
    for setting in setting_references.keys():
        settings[setting[0]][setting[1]] = setting_references[(setting[0], setting[1])].get()

    save_settings_file(settings)

def save_settings_file(settings):
    '''Saves input settings to tabs.ini.'''
    with open('tabs.ini', 'w+') as settings_file:
        settings_file.write('# Settings file for TABS\n\n')
        settings_file.write('# Change this manually here, or\n')
        settings_file.write('# you can use the in-game menu!\n\n')
        settings.write(settings_file)
    logging.info('Saved settings file.')

def reset_settings_file():
    '''Resets the settings file to default.'''
    settings = configparser.ConfigParser()
    settings = globals.default_config
    
    save_settings_file(settings)

def reset_settings_file_handler():
    import globals
    '''Handles calling reset_settings_file() after a confirmation prompt.'''
    if show_ask_question('TABS Settings', 'Are you sure you wish to reset ALL settings to default?'):
        reset_settings_file()
        display_settings_window(globals.main_window_reference)