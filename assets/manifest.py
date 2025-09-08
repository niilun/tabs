from enum import Enum
from units import unit_registry

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
    DARK_LOGO_BACKGROUND = AssetInfo('dark-logo-background', 'image', 'assets/dark/logo-background.png')
    LIGHT_LOGO_BACKGROUND = AssetInfo('light-logo-background', 'image', 'assets/light/logo-background.png')

    # UI assets
    UI_ABILITIES_ICON = AssetInfo('abilities-icon', 'image', 'assets/ui/abilities.png')
    UI_ATTRIBUTES_ICON = AssetInfo('attributes-icon', 'image', 'assets/ui/attributes.png')
    UI_DAMAGE_ICON = AssetInfo('damage-icon', 'image', 'assets/ui/damage.png')
    UI_DESCRIPTION_ICON = AssetInfo('description-icon', 'image', 'assets/ui/description.png')
    UI_EXIT_ICON = AssetInfo('exit-icon', 'image', 'assets/ui/exit.png')
    UI_HEALTH_ICON = AssetInfo('health-icon', 'image', 'assets/ui/health.png')
    UI_INFO_ICON = AssetInfo('info-icon', 'image', 'assets/ui/info.png')
    UI_NEXT_ICON = AssetInfo('next-icon', 'image', 'assets/ui/next.png')
    UI_SETTINGS_SLIDER_ICON = AssetInfo('settings-sliders-icon', 'image', 'assets/ui/settings-sliders.png')
    UI_SETTINGS_ICON = AssetInfo('settings-icon', 'image', 'assets/ui/settings.png')
    UI_SLOT_EMPTY_ICON = AssetInfo('slot-empty', 'image', 'assets/ui/slot-empty.png')

    # Unit attack styles
    UI_ATTACK_STYLE_MELEE = AssetInfo('melee-attack-style', 'image', 'assets/units/attack-styles/melee.png')
    UI_ATTACK_STYLE_RANGED = AssetInfo('ranged-attack-style', 'image', 'assets/units/attack-styles/ranged.png')
    UI_ATTACK_STYLE_MAGIC = AssetInfo('magic-attack-style', 'image', 'assets/units/attack-styles/magic.png')

    # Unit types
    UI_TYPE_LIGHT = AssetInfo('light-type', 'image', 'assets/units/types/light.png')
    UI_TYPE_MEDIUM = AssetInfo('medium-type', 'image', 'assets/units/types/medium.png')
    UI_TYPE_HEAVY = AssetInfo('heavy-type', 'image', 'assets/units/types/heavy.png')
    
    # Unit attributes
    UI_ATTRIBUTE_CAVALRY = AssetInfo('cavalry-attribute', 'image', 'assets/units/attributes/cavalry.png')
    UI_ATTRIBUTE_ANTI_CAVALRY = AssetInfo('anti-cavalry-attribute', 'image', 'assets/units/attributes/anti-cavalry.png')
    UI_ATTRIBUTE_SHIELDED = AssetInfo('shielded-attribute', 'image', 'assets/units/attributes/shielded.png')
    
    # Unit icons
    UNIT_PLACEHOLDER_ICON = AssetInfo('unit-placeholder', 'image', 'assets/units/placeholder.png')
    UNIT_ARCHER_ICON = AssetInfo('unit-archer', 'image', 'assets/units/archer.png')
    UNIT_FIRE_WIZARD_ICON = AssetInfo('unit-fire-wizard', 'image', 'assets/units/fire-wizard.png')
    UNIT_MAN_AT_ARMS_ICON = AssetInfo('unit-man-at-arms', 'image', 'assets/units/man-at-arms.png')
    UNIT_SHIELD_BEARER_ICON = AssetInfo('unit-shield-bearer','image', 'assets/units/shield-bearer.png')
    UNIT_SPEARMAN_ICON = AssetInfo('unit-spearman', 'image', 'assets/units/spearman.png')
    UNIT_WARRIOR_ICON = AssetInfo('unit-warrior', 'image', 'assets/units/warrior.png')

unit_icons_map = {
    'Archer': Asset.UNIT_ARCHER_ICON,
    'Fire Wizard': Asset.UNIT_FIRE_WIZARD_ICON,
    'Shield Bearer': Asset.UNIT_SHIELD_BEARER_ICON,
    'Spearman': Asset.UNIT_SPEARMAN_ICON,
    'Man-at-Arms': Asset.UNIT_MAN_AT_ARMS_ICON,
    'Warrior': Asset.UNIT_WARRIOR_ICON
}

unit_attack_styles_map = {
    'Melee': Asset.UI_ATTACK_STYLE_MELEE,
    'Ranged': Asset.UI_ATTACK_STYLE_RANGED,
    'Magic': Asset.UI_ATTACK_STYLE_MAGIC
}

unit_types_map = {
    'Light': Asset.UI_TYPE_LIGHT,
    'Medium': Asset.UI_TYPE_MEDIUM,
    'Heavy': Asset.UI_TYPE_HEAVY
}

unit_attributes_map = {
    'Cavalry': Asset.UI_ATTRIBUTE_CAVALRY,
    'Anti-Cavalry': Asset.UI_ATTRIBUTE_ANTI_CAVALRY,
    'Shielded': Asset.UI_ATTRIBUTE_SHIELDED
}