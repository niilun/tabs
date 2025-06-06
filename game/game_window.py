import logging, sys
import customtkinter as ctk
from CTkListbox import CTkListbox
from PIL import Image
from .utilities import show_error

# Disable PIL logging
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)

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
        if selected_unit == None:
            return
    except Exception:
        # Tcl throws an error if there's no listbox selection, so we just return without clogging the console
        return
    
    try:
        create_unit(selected_unit, team)
    except Exception as error_message:
        show_error('Error while creating unit', error_message)

def take_next_action_ui_wrapper():
    '''Handler function to run take_next_action()'''
    from game.unit_management import take_next_action

    try:
        take_next_action()
    except Exception as error_message:
        show_error('Error while creating unit', error_message)

def update_scoreboard():
    '''Updates the scoreboard (battle info), checks for new units or the death of existing ones.'''
    from game.unit_management import active_units_team_1, active_units_team_2
    # Function that resets the given slot to default (called if a unit dies)
    def set_default_slot(slot):
        try:
            slot['name'].configure(text = 'Empty slot')
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
                info_slot['name'].configure(text=f'{unit.unit_name[:11].strip()}...')
            else:
                info_slot['name'].configure(text=unit.unit_name)
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
                info_slot['name'].configure(text=f'{unit.unit_name[:11].strip()}...')
            else:
                info_slot['name'].configure(text=unit.unit_name)
            info_slot['health'].delete('all')
            info_slot['health'].create_rectangle(0, 0, 80 * unit_health_percent, 20, fill = 'green')
            info_slot['health'].create_rectangle(80 * unit_health_percent, 0, 80, 20, fill = 'red')
            if unit.armor > 0:
                unit_armor_percent = unit.armor / unit.max_health
                info_slot['health'].create_rectangle(0, 0, 80 * unit_armor_percent, 20, fill = 'yellow')

    logging.info('Updated battle scoreboard.')

def display_main_window():
    '''Creates and shows the game window.'''
    from .unit_management import all_units_map
    from .unit_info_displays import display_unit_stats
    from .settings_window import display_settings_window
    from .utilities import reload_game
    import globals
    import configparser

    global unit_select_input

    config = configparser.ConfigParser()
    config.read('tabs.ini')
    version = config['Game']['Version']

    main_window = ctk.CTk()
    main_window.title('TABS')
    
    globals.main_window_reference = main_window

    main_window.geometry('920x640')
    main_window.resizable(False, False)

    unit_select_frame = ctk.CTkFrame(main_window)
    unit_select_input = CTkListbox(unit_select_frame)
    for unit in all_units_map.keys():
        unit_select_input.insert(ctk.END, unit)
    
    unit_select_input.pack(side = 'left', fill = 'both', expand = True)
    unit_select_frame.pack(side = 'left', fill = 'y', anchor = 'nw', expand = True)

    # Summon buttons for both teams
    ctk.CTkButton(main_window, text = 'Summon', width = 80, command = lambda: create_unit_ui_wrapper(1)).place(x = 190, y = 220)
    ctk.CTkButton(main_window, text = 'Summon', width = 80, command = lambda: create_unit_ui_wrapper(2)).place(x = 190, y = 383)

    take_next_action_icon = ctk.CTkImage(light_image = Image.open('assets/ui/next.png'))
    take_next_action_button = ctk.CTkButton(main_window, text = 'Take next action', image = take_next_action_icon, compound = 'left', command = take_next_action_ui_wrapper)

    take_next_action_button.place(x = 500, y = 80)

    # Unit info bars
    battle_info = ctk.CTkFrame(main_window, fg_color = 'transparent')
    battle_info.place(x = 300, y = 120)

    # Create two rows of 5 frames linked to battle_info
    for i in range(2):
        battle_info.grid_rowconfigure(i, minsize=200, weight=1)
        for j in range(5):
            battle_info.grid_columnconfigure(j, minsize=120, weight=1)

            frame = ctk.CTkFrame(battle_info, width = 120, height = 200)

            # Selection for unit info
            unit_selection_overlay = ctk.CTkButton(frame, width = 200, height = 200, text = '', hover = True, fg_color = 'transparent')
            unit_selection_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

            # Use a placeholder file until an actual unit fills the slot
            unit_image_res = ctk.CTkImage(light_image=Image.open('assets/units/placeholder.png'), size = (100, 100))
            unit_image = ctk.CTkLabel(frame, text = '', width = 80, image = unit_image_res)

            unit_health = ctk.CTkCanvas(frame, height=15, width= 80, background='gray')
            unit_name = ctk.CTkLabel(frame, text='Empty slot', width = 80)

            unit_effects = ctk.CTkFrame(frame, height= 15, width = 90)
            
            unit_image.pack(expand = True)
            unit_name.pack()
            unit_effects.pack()
            unit_health.pack(pady = (0, 4))

            widget_dict = {
                'image': unit_image,
                'name': unit_name,
                'effects': unit_effects,
                'health': unit_health
            }

            if i == 0:
                widgets_team_1.append(widget_dict)
            elif i == 1:
                widgets_team_2.append(widget_dict)

            frame.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

    # Utilities
    quit_button_icon = ctk.CTkImage(light_image = Image.open('assets/ui/exit.png'))
    quit_button = ctk.CTkButton(main_window, text = 'Quit', image = quit_button_icon, width = 80, compound = 'left', command = sys.exit)
    quit_button.place(x = 190, rely = 1, y = -20, anchor = 'w')

    settings_button_icon = ctk.CTkImage(light_image = Image.open('assets/ui/settings-sliders.png'))
    settings_button = ctk.CTkButton(main_window, text = 'Settings', image = settings_button_icon, width = 80, compound = 'left', command = lambda: display_settings_window(main_window))
    settings_button.place(x = 275, rely = 1, y = -20, anchor = 'w')

    unit_info_button_icon = ctk.CTkImage(light_image = Image.open('assets/ui/info.png'))
    unit_info_button = ctk.CTkButton(main_window, text = 'Unit info', image = unit_info_button_icon, width = 100, compound = 'left', command = lambda: display_unit_stats(main_window, unit_select_input))
    unit_info_button.place(x = 368, rely = 1, y = -20, anchor = 'w')

    reload_game_button = ctk.CTkButton(main_window, text = 'Reload', width = 60, command = reload_game)
    reload_game_button.place(x = 850, rely = 0, y = 20, anchor = 'w')

    version_indicator = ctk.CTkLabel(main_window, text = f'v{version}')
    version_indicator.place(x = 880, rely = 1, y = -10, anchor = 'w')

    logging.info('Main window loaded.')
    main_window.mainloop()