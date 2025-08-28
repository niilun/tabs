import customtkinter as ctk, logging, sys, globals, configparser
from CTkListbox import CTkListbox
from PIL import Image

from assets.manifest import Asset

from utilities.window_infoboxes import show_error
from utilities.reload_game import reload_game

from .unit_info_displays import display_unit_stats
from .settings_window import display_settings_window
from .battle_info import create_battle_info

from game.mechanics.status_effects import status_effects

from game.unit_management import active_units_team_1, active_units_team_2
from units import unit_registry

# Disable PIL logging
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)

# Holder for battle info widgets
widgets_team_1 = []
widgets_team_2 = []

# Holders for selective summoning
selected_overlay = None
selected_unit_row = None
selected_unit_column = None

# Wrappers for game actions
def create_unit_ui_wrapper(team: int):
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
        show_error('Error while handling unit creation', error_message)

def take_next_action_ui_wrapper():
    '''Handler function to run take_next_action()'''
    from game.unit_management import take_next_action

    try:
        take_next_action()
    except Exception as error_message:
        show_error('Error while creating unit', error_message)

def update_team_slots(team, widgets):
    # Function that resets the given slot to default (called if a unit dies)
    def set_default_slot(slot):
        try:
            slot['name'].configure(text = 'Empty slot')
            slot['health'].delete('all')
            slot['health'].create_rectangle(0, 0, 80, 20, fill = 'gray')
        except Exception:
            raise Exception(f'Invalid slot call {slot} in {__name__}')
        
    for slot, unit in team.items():
        info_slot = widgets[slot - 1]
        
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

            # update effects
            for widget in info_slot['effects'].winfo_children():
                widget.destroy()
            if unit.effects:
                for effect in list(unit.effects.keys()):
                    match effect:
                        case status_effects.BURN:
                            ctk.CTkLabel(info_slot['effects'], text = 'BRN', height = 10, text_color = 'orange').pack(side = 'left', padx = 2)
                        case status_effects.POISON:
                            ctk.CTkLabel(info_slot['effects'], text = 'PSN', height = 10, text_color = 'lime').pack(side = 'left', padx = 2)
                        case status_effects.VENOM:
                            ctk.CTkLabel(info_slot['effects'], text = 'VEN', height = 10, text_color = 'purple').pack(side = 'left', padx = 2)
                        case status_effects.BLEEDING:
                            ctk.CTkLabel(info_slot['effects'], text = 'BLD', height = 10, text_color = 'red').pack(side = 'left', padx = 2)
                        case status_effects.STUNNED:
                            ctk.CTkLabel(info_slot['effects'], text = 'STN', height = 10, text_color = 'gold').pack(side = 'left', padx = 2)
                        case status_effects.FROZEN:
                            ctk.CTkLabel(info_slot['effects'], text = 'FRZ', height = 10, text_color = 'cyan').pack(side = 'left', padx = 2)
                        case status_effects.DEFENCELESS:
                            ctk.CTkLabel(info_slot['effects'], text = 'DFL', height = 10, text_color = 'gray').pack(side = 'left', padx = 2)
                        case status_effects.DROWSY:
                            ctk.CTkLabel(info_slot['effects'], text = 'DRW', height = 10, text_color = 'light blue').pack(side = 'left', padx = 2)
                        case status_effects.SLEEPY:
                            ctk.CTkLabel(info_slot['effects'], text = 'SLP', height = 10, text_color = 'blue').pack(side = 'left', padx = 2)
                        case status_effects.ASLEEP:
                            ctk.CTkLabel(info_slot['effects'], text = 'ZZZ', height = 10, text_color = 'navy').pack(side = 'left', padx = 2)
                        case status_effects.CONFUSED:
                            ctk.CTkLabel(info_slot['effects'], text = 'CNF', height = 10, text_color = 'magenta').pack(side = 'left', padx = 2)
                        case status_effects.BLINDED:
                            ctk.CTkLabel(info_slot['effects'], text = 'BLN', height = 10, text_color = 'black').pack(side = 'left', padx = 2)
                        case status_effects.SILENCED:
                            ctk.CTkLabel(info_slot['effects'], text = 'SIL', height = 10, text_color = 'dark gray').pack(side = 'left', padx = 2)
            
            if unit.armor > 0:
                unit_armor_percent = unit.armor / unit.max_health
                info_slot['health'].create_rectangle(0, 0, 80 * unit_armor_percent, 20, fill = 'yellow')

def show_turn_indicator():
    '''Finds the unit whose turn is next and passes that to display_unit_turn_incoming for display.'''
    from game.unit_management import turn_counter, get_total_active_units
    from game.unit_info_displays import display_unit_turn_incoming

    # Reset all widgets to inactive
    for widget in widgets_team_1 + widgets_team_2:
        widget['turn_indicator'].itemconfig(1, fill = 'gray', outline = 'gray')

    # Find which team's turn it is
    if turn_counter <= get_total_active_units(1):
        id = turn_counter - 1
        if id < len(widgets_team_1):
            logging.debug(f'Sent widget id {id} on team 1 for indicator update')
            display_unit_turn_incoming(widgets_team_1[id]['turn_indicator'])
        return
    if turn_counter <= get_total_active_units(1) + get_total_active_units(2):
        id = turn_counter - get_total_active_units(1) - 1
        if id < len(widgets_team_2):
            logging.debug(f'Sent widget id {id} on team 2 for indicator update')
            display_unit_turn_incoming(widgets_team_2[id]['turn_indicator'])
        return

def update_scoreboard():
    '''Updates the scoreboard (battle info), checks for new units or the death of existing ones.'''
    from game.unit_management import active_units_team_1, active_units_team_2
    
    update_team_slots(active_units_team_1, widgets_team_1)
    update_team_slots(active_units_team_2, widgets_team_2)
    show_turn_indicator()

def show_overlay_selected(row: int, column: int, clear_unit_selection_button_reference):
    '''Sets one of the unit slots as selected. The previous one gets unset.'''
    global selected_overlay, selected_unit_row, selected_unit_column
    if selected_overlay != None:
        selected_overlay['info_selection'].configure(fg_color='transparent')

    selected_unit_row = row
    selected_unit_column = column
                
    if row == 0:
        selected_overlay = widgets_team_1[column]
        selected_overlay['info_selection'].configure(fg_color='gray')
        clear_unit_selection_button_reference.configure(fg_color='#3a7ebf', hover_color = '#325882')
    elif row == 1:
        selected_overlay = widgets_team_2[column]
        selected_overlay['info_selection'].configure(fg_color='gray')
        clear_unit_selection_button_reference.configure(fg_color='#3a7ebf', hover_color = '#325882')
    else:
        raise Exception(f'Invalid row call {row} in {__name__}!')

def clear_selected_overlay(clear_unit_selection_button_reference):
    '''Clears the current unit selection (if it exists).'''
    global selected_overlay
    if selected_overlay != None:
        clear_unit_selection_button_reference.configure(fg_color='gray', hover_color = 'gray')
        selected_overlay['info_selection'].configure(fg_color='transparent')
        selected_overlay = None

def display_main_window():
    '''Creates and shows the game window.'''
    global unit_select_input

    config = globals.loaded_config
    version = config['Game']['Version']

    main_window = ctk.CTk()
    main_window.title('TABS')
    
    globals.main_window_reference = main_window

    main_window.geometry('920x640')
    main_window.resizable(False, False)

    unit_select_frame = ctk.CTkFrame(main_window)
    unit_select_input = CTkListbox(unit_select_frame)
    for unit in unit_registry.keys():
        unit_select_input.insert(ctk.END, unit)
    
    unit_select_input.pack(side = 'left', fill = 'both', expand = True)
    unit_select_frame.pack(side = 'left', fill = 'y', anchor = 'nw', expand = True)

    # Summon buttons for both teams
    ctk.CTkButton(main_window, text = 'Summon', width = 80, command = lambda: create_unit_ui_wrapper(1)).place(x = 200, y = 200)
    ctk.CTkButton(main_window, text = 'Summon', width = 80, command = lambda: create_unit_ui_wrapper(2)).place(x = 200, y = 420)

    take_next_action_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_NEXT_ICON.path))
    take_next_action_button = ctk.CTkButton(main_window, text = 'Take next action', image = take_next_action_icon, compound = 'left', command = take_next_action_ui_wrapper)

    take_next_action_button.place(x = 500, y = 80)

    # Utilities
    quit_button_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_EXIT_ICON.path))
    quit_button = ctk.CTkButton(main_window, text = 'Quit', image = quit_button_icon, width = 80, compound = 'left', command = sys.exit)
    quit_button.place(x = 190, rely = 1, y = -20, anchor = 'w')

    settings_button_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_SETTINGS_SLIDER_ICON.path))
    settings_button = ctk.CTkButton(main_window, text = 'Settings', image = settings_button_icon, width = 80, compound = 'left', command = lambda: display_settings_window(main_window))
    settings_button.place(x = 275, rely = 1, y = -20, anchor = 'w')

    unit_info_button_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_INFO_ICON.path))
    unit_info_button = ctk.CTkButton(main_window, text = 'Unit info', image = unit_info_button_icon, width = 100, compound = 'left', command = lambda: display_unit_stats(main_window, unit_select_input, active_units_team_1, widgets_team_1, active_units_team_2, widgets_team_2, selected_unit_row, selected_unit_column))
    unit_info_button.place(x = 368, rely = 1, y = -20, anchor = 'w')

    clear_selection_button = ctk.CTkButton(main_window, text = 'Clear unit selection', hover_color = 'gray', bg_color = 'transparent', fg_color = 'gray', width = 100, command = lambda: clear_selected_overlay(clear_selection_button))
    clear_selection_button.place(x = 720, rely = 0, y = 20, anchor = 'w')

    reload_game_button = ctk.CTkButton(main_window, text = 'Reload', width = 60, command = reload_game)
    reload_game_button.place(x = 850, rely = 0, y = 20, anchor = 'w')

    version_indicator = ctk.CTkLabel(main_window, text = f'v{version}')
    version_indicator.place(x = 880, rely = 1, y = -10, anchor = 'w')

    # pass the unit selection so we know to set it blue, when a unit is selected
    create_battle_info(clear_selection_button)

    logging.info('Main window loaded.')
    main_window.mainloop()