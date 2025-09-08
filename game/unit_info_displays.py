import customtkinter as ctk, logging, globals

from PIL import Image
from assets.manifest import Asset, unit_types_map, unit_attributes_map, unit_attack_styles_map, unit_icons_map

from units import unit_registry

def display_unit_stats(main_window, unit_select_input, active_units_team_1, widgets_team_1, active_units_team_2, widgets_team_2, selected_unit_row, selected_unit_column):
    '''Shows stats of selected unit in an info window.'''
    using_battling_unit = False
    
    # if a unit in the left row is selected, set it first
    selected_unit = unit_select_input.get(unit_select_input.curselection())

    if selected_unit != None:
        selected_unit = unit_registry[selected_unit]()

    # if a battling unit is selected, set it, overriding the first (unless the slot is empty)
    if selected_unit_row == 0 and str(widgets_team_1[selected_unit_column]['name'].cget('text')) != 'Empty slot':
        selected_unit = active_units_team_1[selected_unit_column + 1]
        using_battling_unit = True
    elif selected_unit_row == 1 and str(widgets_team_2[selected_unit_column]['name'].cget('text')) != 'Empty slot':
        selected_unit = active_units_team_2[selected_unit_column + 1]
        using_battling_unit = True
    
    # if none are selected, return
    if selected_unit == None:
        return
    
    # If the window already exists, reuse it. Otherwise, create it
    if globals.stat_window_active and globals.stat_window_active.winfo_exists():
        stat_window = globals.stat_window_active
        for child in stat_window.winfo_children():
            child.destroy()
        stat_window.deiconify()
        stat_window.lift()
    else:
        stat_window = ctk.CTkToplevel(main_window)
        stat_window.geometry('500x320')
        stat_window.resizable(False, False)
        stat_window.protocol('WM_DELETE_WINDOW', lambda: stat_window.withdraw())

        # Store the window for later use
        globals.stat_window_active = stat_window

    stat_window.title(f'Unit info // {selected_unit.unit_name}')

    try:
        # get unit icon
        unit_image_path = unit_icons_map.get(selected_unit.unit_name).path
        unit_image = ctk.CTkImage(light_image = Image.open(unit_image_path), size = (128, 128))
        unit_image_label = ctk.CTkLabel(stat_window, text = '', image = unit_image)
    except Exception:
        logging.warning(f"Unit icon not mapped, using placeholder")
        unit_image = ctk.CTkImage(light_image = Image.open(Asset.UNIT_PLACEHOLDER_ICON.path), size = (128, 128))
        unit_image_label = ctk.CTkLabel(stat_window, text = '', image = unit_image)
    
    unit_image_label.place(x = 2, y = 100)

    # Line separator
    image_sep = ctk.CTkCanvas(stat_window, width = 2, height = 320)
    image_sep.create_rectangle(0, 0, 2, 320, fill = 'gray')
    image_sep.place(x = 132, y = 0)

    # UNIT STATS
    stat_frame = ctk.CTkFrame(stat_window, width = 170, height = 120)
    stat_frame.place(x = 140, y = 10)
    stat_frame.grid_propagate(False)
    stat_frame.pack_propagate(False)

    # find the unit's attack style and get the respective UI icon
    attack_style_path = unit_attack_styles_map.get(selected_unit.attack_style).path
    attack_style_label_image = ctk.CTkImage(light_image = Image.open(attack_style_path))
    attack_style_label = ctk.CTkLabel(stat_frame, text = f' {selected_unit.attack_style}', compound = 'left', image = attack_style_label_image)
    attack_style_label.grid(row = 0, column = 0, padx = (5, 0), pady = 5, sticky = 'w')

    # find the unit's type and get the respective UI icon
    type_path = unit_types_map.get(selected_unit.type).path
    type_image = ctk.CTkImage(light_image = Image.open(type_path))
    type_label = ctk.CTkLabel(stat_frame, text = f' {selected_unit.type}', compound = 'left', image = type_image)
    type_label.grid(row = 0, column = 1, padx = (0, 5), pady = 5, sticky = 'w')

    stat_separator = ctk.CTkCanvas(stat_frame, width = 170, height = 1)
    stat_separator.create_rectangle(0, 0, 170, 1, fill = 'gray')
    stat_separator.grid(row = 1, column = 0, columnspan = 3)

    # if using a unit selected from the left side selection bar, we don't need to repeat the same HP value twice
    if using_battling_unit:
        unit_armor = selected_unit.armor if selected_unit.armor > 0 else 0
        unit_health = int(selected_unit.current_health) + unit_armor
        unit_max_health = int(selected_unit.max_health)

        health_text = f' {unit_health} / {unit_max_health} HP'
    else:
        health_text = f' {selected_unit.current_health} health'
    
    health_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_HEALTH_ICON.path))
    health_label = ctk.CTkLabel(stat_frame, text = health_text, compound = 'left', image = health_icon)
    health_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')

    attack_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_DAMAGE_ICON.path))
    attack_label = ctk.CTkLabel(stat_frame, text = f' {int(selected_unit.attack_damage)} damage', compound = 'left', image = attack_icon)
    attack_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'w')

    # ABILITIES
    # if they are defined manually in an abilties list, use that
    abilities = []
    try:
        abilities = ', '.join(selected_unit.abilities)
    # otherwise, scan the unit's functions for ones that start with 'ability_' and use that
    except AttributeError:
        for function in dir(selected_unit):
            if callable(getattr(selected_unit, function)):
                if function.startswith('ability_'):
                    abilities.append(function.upper())
        abilities = ', '.join(abilities)

    abilities_frame = ctk.CTkFrame(stat_window, width = 170, height = 100)
    abilities_frame.place(x = 320, y = 10)
    abilities_frame.pack_propagate(False)
    abilities_frame.grid_propagate(False)

    abilities_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_ABILITIES_ICON.path))
    abilities_display = ctk.CTkLabel(abilities_frame, padx = 5, pady = 9, image = abilities_icon, compound = 'left', text = f'Abilities')
    abilities_display.grid(row = 0, column = 0)

    abilities_separator = ctk.CTkCanvas(abilities_frame, width = 170, height = 10)
    abilities_separator.create_rectangle(0, 0, 170, 1, fill = 'gray')
    abilities_separator.grid(row = 1, column = 0)

    abilities_list = ctk.CTkLabel(abilities_frame, text = abilities)
    abilities_list.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nsew')

    logging.info(f'Showing unit info for {selected_unit.unit_name}')

    # ATTRIBUTES
    attributes_frame = ctk.CTkFrame(stat_window, width = 170, height = 120)
    attributes_frame.place(x = 140, y = 140)
    attributes_frame.pack_propagate(False)

    attributes_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_ATTRIBUTES_ICON.path))
    attributes_display = ctk.CTkLabel(attributes_frame, padx = 5, pady = 9, image = attributes_icon, compound = 'left', text = f'Attributes')
    attributes_display.grid(row = 0, column = 0)

    attributes_separator = ctk.CTkCanvas(attributes_frame, width = 170, height = 10)
    attributes_separator.create_rectangle(0, 0, 170, 1, fill = 'gray')
    attributes_separator.grid(row = 1, column = 0)

    # list unit attributes
    if len(selected_unit.attributes) == 0:
        # if no attributes, display none
        attribute_image = Asset.UI_EXIT_ICON.path
        attribute_image = ctk.CTkImage(light_image = Image.open(attribute_image))

        attribute_display = ctk.CTkLabel(attributes_frame, padx = 5, pady = 5, image = attribute_image, compound = 'left', text = 'None')
        attribute_display.grid(row = 2, column = 0, sticky = 'nsew')
    else:
        current_row = 2
        # for each attribute, get its icon from the map and list it
        for attribute in selected_unit.attributes:
            attribute_image = unit_attributes_map.get(attribute).path
            attribute_image = ctk.CTkImage(light_image = Image.open(attribute_image))

            attribute_display = ctk.CTkLabel(attributes_frame, padx = 5, pady = 5, image = attribute_image, compound = 'left', text = attribute)
            attribute_display.grid(row = current_row, column = 0, sticky = 'nsew')
            current_row += 1

    # UNIT DESCRIPTION
    description_frame = ctk.CTkFrame(stat_window, width = 170, height = 120)
    description_frame.place(x = 320, y = 120)
    description_frame.pack_propagate(False)

    description_icon = ctk.CTkImage(light_image = Image.open(Asset.UI_DESCRIPTION_ICON.path))
    description_display = ctk.CTkLabel(description_frame, padx = 5, pady = 9, image = description_icon, compound = 'left', text = f'Description')
    description_display.grid(row = 0, column = 0)

    description_separator = ctk.CTkCanvas(description_frame, width = 170, height = 10)
    description_separator.create_rectangle(0, 0, 170, 1, fill = 'gray')
    description_separator.grid(row = 1, column = 0)

    # get unit description
    try:
        description = selected_unit.description
    except AttributeError:
        description = 'None.'
    
    description_text = ctk.CTkLabel(description_frame, padx = 5, pady = 5, text = description, wraplength=160, justify='left')
    description_text.grid(row = 2, column = 0, sticky = 'nsew')

def display_unit_turn_incoming(widget):
    '''Updates given widget to indicate an incoming turn'''
    widget.create_oval(1, 1, 10, 10, fill = 'green', outline = 'green')