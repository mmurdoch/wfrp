from command import *
from wfrp import *

class RollCommand(Command):
    def __init__(self):
        super(RollCommand, self).__init__('roll')

    @property
    def short_help(self):
        return 'Rolls a die'

    @property
    def long_help(self):
        return (
            '  roll d10  - rolls a ten-sided die\n' +
            '  roll d100 - rolls a one hundred-sided die')

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing die')

        die = command_parts[0]
        if die == 'd10':
            print(roll_d10())
        elif die == 'd100':
            print(roll_d100())
        else:
            raise ValueError('Unknown die ' + die)
