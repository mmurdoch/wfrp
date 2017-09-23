from command import *
from addcommand import *
from helpcommand import *
from commandhelpcommand import *
from generatecommand import *
from listcommand import *
from showcommand import *
from gotocommand import *
from attackcommand import *
from wfrp import *


class CommandExecutor(object):
    def __init__(self, wfrp=None):
        if not wfrp:
            wfrp = Wfrp()
        self._wfrp = wfrp
        self._save_after_successful_command = False

        command_help_command = CommandHelpCommand()
        help_command = self.create_help_command()
        commands = [
            command_help_command,
            help_command,
            AddCommand(),
            GenerateCommand(),
            ListCommand(),
            ShowCommand(),
            GotoCommand(),
            AttackCommand()
        ]
        command_help_command.commands = commands
        help_command.commands = commands
        self._commands = commands

    def execute_command(self, command_parts):
        if len(command_parts) == 0:
            command_name = self.create_help_command().name 
        else: 
            command_name = command_parts[0]

        command = find_command(self.commands, command_name)
        if not command:
            raise ValueError('Unknown command: ' + command_name)

        command.execute(self._wfrp, command_parts[1:])

        if self.save_after_successful_command:
            self._wfrp.save()

    def create_help_command(self):
        return HelpCommand()

    @property
    def commands(self):
        return self._commands

    @property
    def save_after_successful_command(self):
        return self._save_after_successful_command

    @save_after_successful_command.setter
    def save_after_successful_command(self, value):
        self._save_after_successful_command = value
