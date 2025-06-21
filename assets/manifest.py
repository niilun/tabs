from enum import Enum

class AssetInfo:
    '''Class for assets to store their info.'''
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path

    def __repr__(self):
        return f'AssetInfo | name {self.name} | type {self.type} | path {self.path}'

class Asset(Enum):
    '''The asset manifest defines all assets, their type and path location (relative to main.py)'''

    # adds a .path property to the Enum
    @property
    def path(self):
        return self.value.path
    
    # Light/Dark type assets
    DARK_LOGO_BACKGROUND = AssetInfo('dark_logo_background', 'image', 'assets/dark/logo_background.png')
    LIGHT_LOGO_BACKGROUND = AssetInfo('light_logo_background', 'image', 'assets/light/logo_background.png')

    # UI assets
    UI_ABILITIES_ICON = AssetInfo('abilities_icon', 'image', 'assets/ui/abilities.png')
    UI_ATTACK_ICON = AssetInfo('attack_icon', 'image', 'assets/ui/attack.png')
    UI_EXIT_ICON = AssetInfo('exit_icon', 'image', 'assets/ui/exit.png')
    UI_HEALTH_ICON = AssetInfo('health_icon', 'image', 'assets/ui/health.png')
    UI_INFO_ICON = AssetInfo('info_icon', 'image', 'assets/ui/info.png')
    UI_NEXT_ICON = AssetInfo('next_icon', 'image', 'assets/ui/next.png')
    UI_SETTINGS_SLIDER_ICON = AssetInfo('settings_sliders_icon', 'image', 'assets/ui/settings_sliders.png')
    UI_SETTINGS_ICON = AssetInfo('settings_icon', 'image', 'assets/ui/settings.png')

    # Unit icons
    UNIT_PLACEHOLDER_ICON = AssetInfo('unit_placeholder', 'image', 'assets/units/placeholder.png')
