def find_command(commands, command_name):
    for command in commands:
        if command.name == command_name:
            return command

    return None

def check_current_campaign(wfrp):
    if not wfrp.current_campaign:
        raise ValueError('No current campaign') 

def check_current_encounter(wfrp):
    check_current_campaign(wfrp)
    if not wfrp.current_campaign.current_encounter:
        raise ValueError('No current encounter')

class Command(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
