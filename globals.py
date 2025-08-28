import configparser

# Window holders
# These variables hold windows so the same button doesn't spawn more than one of each at once
stat_window_active = None
settings_window_active = None

# Settings
loaded_config = None

# Window references
main_window_reference = None
last_game_event_text_reference = None

default_config = configparser.ConfigParser()
default_config.optionxform = str # stop configparser from lowering config names

default_config['Game'] = {'Version': '1.0.0',
                          'UnitHealthScaling': 1,
                          'UnitAttackScaling': 1
                          }
default_config['Network'] = {'PerformUpdateCheck': 'true',
                             'RepositoryData': 'niilun/tabs'
                             }
default_config['Debug'] = {'DebugLevel': 20}