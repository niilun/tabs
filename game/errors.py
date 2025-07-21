class UnitNotFoundError(Exception):
    """Error class for units that aren't found"""
    def __init__(self, unit):
        self.message = f'Unit {unit} not found!'
        super().__init__(self.message)

class TeamFullError(Exception):
    """Error class for a full team"""
    def __init__(self, team):
        self.message = f'Team {team} is full!'
        super().__init__(self.message)

class TeamsEmptyError(Exception):
    """Error class for empty teams that can't fight"""
    def __init__(self):
        self.message = f'No fights can happen between empty teams! \nAdd some units to both before continuing to take turns.'
        super().__init__(self.message)

class EffectNotFound(Exception):
    """Error class for effects that aren't found"""
    def __init__(self, effect):
        self.message = f'Effect {effect} not found.'
        super().__init__(self.message)