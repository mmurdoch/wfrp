def find_command(commands, command_name):
    for command in commands:
        if command.name == command_name:
            return command

    return None

class Command(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
