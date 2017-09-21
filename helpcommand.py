from command import *

class HelpCommand(Command):
    def __init__(self):
        super(HelpCommand, self).__init__('help')

    @property
    def commands(self):
        return self._commands

    @commands.setter
    def commands(self, value):
        self._commands = value

    @property
    def short_help(self):
        return 'prints this help message'

    @property
    def long_help(self):
        return 'HELP HELP'

    @property
    def max_command_name_length(self):
        max_name_length = 0

        for command in self.commands:
            current_name_length = len(command.name)
            if len(command.name) > max_name_length:
                max_name_length = current_name_length

        return max_name_length

    def pad_command_name(self, command_name):
        return command_name + ' ' * (self.max_command_name_length - len(command_name))

    def execute(self, wfrp, command_parts):
        print('Warhammer Fantasy Roleplaying game assistant')
        print('')

        if len(command_parts) == 0:
            print('Usage: wfrp <command>')
            print('')
            print('Where <command> is one of:')
            print('')
            for command in self.commands:
                print('  ' + self.pad_command_name(command.name) +
                      ' - ' + command.short_help)
        else:
            self.commands[0].execute(wfrp, command_parts)
