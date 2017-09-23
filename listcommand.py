from command import *
from wfrp import *

class ListCommand(Command):
    def __init__(self):
        super(ListCommand, self).__init__('list')

    @property
    def short_help(self):
        return 'Displays elements in the game'

    @property
    def long_help(self):
        return (
            '  list campaigns - displays the campaigns in the game\n' +
            '  list party     - displays the player characters in the current campaign')

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing element type')

        element_type = command_parts[0]
        if element_type == 'campaigns':
            for campaign in wfrp.campaigns:
                print(campaign.name)
        elif element_type == 'party':
            if not wfrp.current_campaign:
                raise ValueError('No current campaign')

            for pc in wfrp.current_campaign.party:
                print(pc.name)
        else:
            raise ValueError('Unknown element type ' + element_type)
