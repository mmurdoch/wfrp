from command import *
from wfrp import *

class AddCommand(Command):
    def __init__(self):
        super(AddCommand, self).__init__('add')

    @property
    def short_help(self):
        return 'adds elements to the game'

    @property
    def long_help(self):
        return (
            '  add campaign <campaign_name> - adds a campaign with the specified name\n' +
            '  add creature <creature_name> <ws> <bs> <s> <t> <ag> <int> <wp> <fel> <w>\n' + '      - adds a creature with the specified characteristics\n' +
            '  add pc <character_name> <ws> <bs> <s> <t> <ag> <int> <wp> <fel> <w>\n' + '      - adds a player character with the specified characteristics\n' + '        to the current campaign\n' +
            '  add encounter <encounter_name> <creature_name> [<creature_name>]*\n' + '     - adds a combat encounter to the current campaign')

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing element')

        element_name = command_parts[0]
        if element_name == 'campaign':
            if len(command_parts) < 2:
                raise ValueError('Missing campaign name')

            wfrp.add_campaign(Campaign(command_parts[1])) 
        elif element_name == 'creature':
            wfrp.add_creature(Creature(
                command_parts[1], int(command_parts[2]),
                int(command_parts[3]), int(command_parts[4]),
                int(command_parts[5]), int(command_parts[6]),
                int(command_parts[7]), int(command_parts[8]),
                int(command_parts[9]), int(command_parts[10]),
                int(command_parts[11]), int(command_parts[12])))
        elif element_name == 'pc':
            check_current_campaign(wfrp)

            wfrp.current_campaign.add_player_character(Character(
                command_parts[1], command_parts[2], int(command_parts[3]),
                int(command_parts[4]), int(command_parts[5]),
                int(command_parts[6]), int(command_parts[7]),
                int(command_parts[8]), int(command_parts[9]),
                int(command_parts[10]), int(command_parts[11]),
                int(command_parts[12]), int(command_parts[13])))
        elif element_name == 'encounter':
            check_current_campaign(wfrp)

            creatures = []
            for creature_name in command_parts[2:]:
                # TODO To ensure that identical creatures are treated
                # separately in combat, need to copy the found creature
                # TODO Write a test for this first!
                creature = wfrp.find_creature(creature_name)
                if not creature:
                    raise ValueError('Cannot add encounter with invalid creature ' + creature_name)

                creatures.append(wfrp.find_creature(creature_name))

            wfrp.current_campaign.add_encounter(Encounter(
                command_parts[1], *creatures))
        else:
            raise ValueError('Cannot add invalid element ' + element_name)
