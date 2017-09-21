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
        return 'add campaign <campaign_name> - adds a campaign with the specified name'

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing element')

        element_name = command_parts[0]
        if element_name != 'campaign':
            raise ValueError('Cannot add invalid element ' + element_name)

        if len(command_parts) < 2:
            raise ValueError('Missing campaign name')

        wfrp.add_campaign(Campaign(command_parts[1])) 
