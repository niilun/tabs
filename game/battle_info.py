import customtkinter as ctk
import globals

from PIL import Image
from assets.manifest import Asset

def create_battle_info(clear_unit_selection_button_reference):
    from game.game_window import widgets_team_1, widgets_team_2, show_overlay_selected

    main_window = globals.main_window_reference
    
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
            unit_selection_overlay = ctk.CTkButton(frame, width = 200, height = 200, text = '', hover = True, fg_color = 'transparent', command = lambda i=i, j=j: show_overlay_selected(i, j, clear_unit_selection_button_reference))
            unit_selection_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

            # Green circle that lights up when it's this unit's turn
            unit_turn_indicator = ctk.CTkCanvas(frame, height = 10, width = 10)

            # Use a placeholder file until an actual unit fills the slot
            unit_image_res = ctk.CTkImage(light_image=Image.open(Asset.UNIT_PLACEHOLDER_ICON.path), size = (100, 100))
            unit_image = ctk.CTkLabel(frame, text = '', width = 80, image = unit_image_res)

            unit_health = ctk.CTkCanvas(frame, height=15, width= 80, background = 'gray')
            unit_name = ctk.CTkLabel(frame, text='Empty slot', width = 80)

            unit_effects = ctk.CTkFrame(frame, height = 15, width = 90)

            unit_image.pack(expand = True)
            unit_name.pack()
            unit_effects.pack()
            unit_health.pack(pady = (0, 4))
            unit_turn_indicator.place(x = 102, y = 0)

            widget_dict = {
                'image': unit_image,
                'name': unit_name,
                'info_selection': unit_selection_overlay,
                'turn_indicator': unit_turn_indicator,
                'effects': unit_effects,
                'health': unit_health
            }

            if i == 0:
                widgets_team_1.append(widget_dict)
            elif i == 1:
                widgets_team_2.append(widget_dict)

            frame.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")