from command import *
from wfrp import *

class GenerateCommand(Command):
    def __init__(self):
        super(GenerateCommand, self).__init__('generate')

    @property
    def short_help(self):
        return 'randomly generates elements for the game'

    @property
    def long_help(self):
        return 'GENERATE GENERATE'

    def execute(self, wfrp, command_parts):
        if not wfrp.current_campaign:
            raise ValueError('No current campaign')

        if len(command_parts) == 0:
            pc_race = wfrp.random_pc_race()
        else:
            pc_race = command_parts[0]

        if pc_race in wfrp.supported_pc_races: 
            pc = Character(pc_race)
            wfrp.current_campaign.add_player_character(pc)
        else:
            raise ValueError('Unsupported PC race: ' + pc_race)
