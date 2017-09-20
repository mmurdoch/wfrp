import json
import random
import sys


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


class AddCommand(Command):
    def __init__(self):
        super(AddCommand, self).__init__('add')

    @property
    def short_help(self):
        return 'adds elements to the game'

    @property
    def long_help(self):
        return 'ADD ADD'

    def execute(self, wfrp, command_parts):
        wfrp.add_campaign(Campaign(command_parts[1])) 


class GenerateCommand(Command):
    def __init__(self):
        super(GenerateCommand, self).__init__('generate')

    @property
    def short_help(self):
        return 'randomly generates elements for the game'

    @property
    def long_help(self):
        return 'GENERATE GENERATE'

    def execute(self, wfrp, command_parts):
        if not wfrp.current_campaign:
            raise ValueError('No current campaign')
        else:
            requested_pc_race = command_parts[1]
            if requested_pc_race in wfrp.supported_pc_races: 
                wfrp.current_campaign.add_player_character(Character(requested_pc_race))
            else:
                raise ValueError('Unsupported PC race: ' + requested_pc_race)


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

class CommandExecutor(object):
    def __init__(self, wfrp=None):
        if not wfrp:
            wfrp = Wfrp()
        self._wfrp = wfrp
        self._save_after_successful_command = False

        command_help_command = CommandHelpCommand()
        help_command = HelpCommand()
        commands = [
            command_help_command,
            help_command,
            AddCommand(),
            GenerateCommand()
        ]
        command_help_command.commands = commands
        help_command.commands = commands
        self._commands = commands

    def execute_command(self, command_parts):
        command_name = command_parts[0]

        command = find_command(self.commands, command_name)
        if not command:
            raise ValueError('Unknown command: ' + command_name)

        command.execute(self._wfrp, command_parts[1:])

        if self.save_after_successful_command:
            self._wfrp.save()


    @property
    def commands(self):
        return self._commands

    @property
    def save_after_successful_command(self):
        return self._save_after_successful_command

    @save_after_successful_command.setter
    def save_after_successful_command(self, value):
        self._save_after_successful_command = value


def to_data_array(array):
    data_array = []
    for element in array:
        data_array.append(element.to_data())

    return data_array

 
class Wfrp(object):
    def __init__(self):
        self._campaigns = []
        self._current_campaign = None

    @property
    def campaigns(self):
        return self._campaigns

    @property
    def current_campaign(self):
        return self._current_campaign

    def add_campaign(self, campaign):
        self._campaigns.append(campaign)
        self._current_campaign = campaign 

    @property
    def supported_pc_races(self):
        return ['elf', 'human']

    def to_data(self):
        return {
            'campaigns': to_data_array(self._campaigns) 
        }

    def save(self):
        with open('wfrp.json', 'w') as data_file:
            data = self.to_data()
            data_file.write(json.dumps(data))

    @staticmethod
    def from_data(data):
        wfrp = Wfrp()
        for element in data['campaigns']:
            campaign = Campaign.from_data(element)
            wfrp.add_campaign(campaign)

        return wfrp 

    @staticmethod
    def load():
        try:
            with open('wfrp.json', 'r') as data_file:
                file_content = data_file.read()
                data = json.loads(file_content)
                return Wfrp.from_data(data)
        except FileNotFoundError:
            return Wfrp()   


class Character(object):
    def __init__(self, race):
        self._race = race

    @property
    def race(self):
        return self._race

    def to_data(self):
        return {
            'race': self.race
        }


class Campaign(object):
    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError('name must be a string, was ' + str(type(name)))
        self._name = name
        self._party = []

    @property
    def name(self):
       return self._name

    def add_player_character(self, character):
        self._party.append(character) 

    @property
    def party(self):
       return self._party 

    def to_data(self):
        return {
            'name': self._name,
            'party': to_data_array(self._party)
        }

    @staticmethod
    def from_data(data):
        return Campaign(data['name'])
