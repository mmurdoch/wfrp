from command import *
from wfrp import *

class GotoCommand(Command):
    def __init__(self):
        super(GotoCommand, self).__init__('goto')

    @property
    def short_help(self):
        return 'Changes the current setting of the game'

    @property
    def long_help(self):
        return (
            '  goto campaign <campaign_name>   - changes the current campaign to the one specified\n' +
            '  goto encounter <encounter_name> - changes the current encounter in the current campaign to the one specified')

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing setting type')

        element_type = command_parts[0]

        found = False
        if element_type == 'campaign':
            if len(command_parts) == 1:
                raise ValueError('Missing ' + element_type + ' name')

            element_name = command_parts[1]

            campaign = wfrp.find_campaign()
            if campaign:
                wfrp.current_campaign = campaign
                found = True
        elif element_type == 'encounter':
            if len(command_parts) == 1:
                raise ValueError('Missing ' + element_type + ' name')

            element_name = command_parts[1]

            check_current_campaign(wfrp)

            encounter = wfrp.current_campaign.find_encounter(element_name)
            if encounter:
                wfrp.current_campaign.current_encounter = encounter
                found = True
        else:
            raise ValueError('Unknown element type ' + element_type)

        if not found:
            raise ValueError('Unknown ' + element_type + ' ' + element_name)
