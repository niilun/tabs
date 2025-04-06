import configparser

update_available = False

# Window holders
# These variables hold windows so the same button doesn't spawn more than one of each at once
stat_window_active = None
settings_window_active = None

# Settings
loaded_config = None

default_config = configparser.ConfigParser()
default_config.optionxform = str # stop configparser from lowering config names

default_config['Game'] = {'Version': '0.7.0',
                          'UnitHealthScaling': 1,
                          'UnitAttackScaling': 1
                          }
default_config['Network'] = {'PerformUpdateCheck': 'true',
                             'RepositoryData': 'niilun/tabs'
                             }
default_config['Debug'] = {'DebugLevel': 20}