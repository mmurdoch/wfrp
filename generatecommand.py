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
            '  generate dwarf    - generates a dwarven player character\n' +
            '  generate elf      - generates an elven player character\n' +
            '  generate halfling - generates a halfling player character\n' +
            '  generate human    - generates a human player character\n' +
            '  generate random   - generates a player character with a random race')

    def execute(self, wfrp, command_parts):
        check_current_campaign(wfrp)

        if len(command_parts) == 0:
            raise ValueError('Missing race')

        pc_race = command_parts[0]
 
        if pc_race == 'random':
            pc_race = wfrp.random_pc_race()

        if pc_race in wfrp.supported_pc_races: 
            name = 'Nobody'
            weapon_skill = 31
            ballistic_skill = 31
            strength = 31
            toughness = 31
            agility = 31
            intelligence = 31
            willpower = 31
            fellowship = 31
            wounds = 11
            weapon_damage = 1
            armour = 0
            pc = Character(
                name, pc_race,
                weapon_skill, ballistic_skill, strength, toughness,
                agility, intelligence, willpower, fellowship, wounds,
                weapon_damage, armour)
            wfrp.current_campaign.add_player_character(pc)
        else:
            raise ValueError('Unsupported PC race: ' + pc_race)
