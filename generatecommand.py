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
        return (
            'generate dwarf    - generates a dwarven player character\n' +
            'generate elf      - generates an elven player character\n' +
            'generate halfling - generates a halfling player character\n' +
            'generate human    - generates a human player character\n' +
            'generate random   - generates a player character with a random race')

    def execute(self, wfrp, command_parts):
        if not wfrp.current_campaign:
            raise ValueError('No current campaign')

        if len(command_parts) == 0:
            raise ValueError('Missing race')

        pc_race = command_parts[0]
 
        if pc_race == 'random':
            pc_race = wfrp.random_pc_race()

        if pc_race in wfrp.supported_pc_races: 
            pc = Character(pc_race)
            wfrp.current_campaign.add_player_character(pc)
        else:
            raise ValueError('Unsupported PC race: ' + pc_race)
