from command import *

class CommandHelpCommand(Command):
    def __init__(self):
        super(CommandHelpCommand, self).__init__('help <command_name>')

    @property
    def commands(self):
        return self._commands

    @commands.setter
    def commands(self, value):
        self._commands = value

    @property
    def short_help(self):
        return 'prints additional help for the specified command'

    def execute(self, wfrp, command_parts):
        command_name = command_parts[0]
        command = find_command(self.commands, command_name)
        if command:
            print(command.long_help)
        else:
            print('Unknown command: ' + command_name)
