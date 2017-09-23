from command import *
from wfrp import *

def percent(value):
    return str(value) + '%'

class ShowCommand(Command):
    def __init__(self):
        super(ShowCommand, self).__init__('show')

    @property
    def short_help(self):
        return 'Displays full details of a game element'

    @property
    def long_help(self):
        return (
            '  show <element_name> - displays details of a game element')

    def print_creature(self, creature):
        print('Characteristics:')
        print('  Weapon Skill:    ' + percent(creature.weapon_skill))
        print('  Ballistic Skill: ' + percent(creature.ballistic_skill))
        print('  Strength:        ' + percent(creature.strength))
        print('  Toughness:       ' + percent(creature.toughness))
        print('  Agility:         ' + percent(creature.agility))
        print('  Intelligence:    ' + percent(creature.intelligence))
        print('  Willpower:       ' + percent(creature.willpower))
        print('  Fellowship:      ' + percent(creature.fellowship))
        print('  Wounds:          ' + str(creature.wounds))

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing element name')

        element_name = command_parts[0]

        found = False
        for creature in wfrp.creatures:
            if creature.name == element_name:
                print('Name: ' + creature.name + ' (creature)')
                self.print_creature(creature)
                found = True

        for campaign in wfrp.campaigns:
            if campaign.name == element_name:
                print('Name: ' + campaign.name + ' (campaign)')
                print('Encounters:')
                for encounter in campaign.encounters:
                    print('  Name: ' + encounter.name)
                    print('  Creatures:')
                    for i, creature in encounter.creatures:
                        print('    Type: ' + creature.name + ' ID: ' + str(i))
 
                found = True

            for pc in campaign.party:
                if pc.name == element_name:
                    print('Name: ' + pc.name + ' (player character)')
                    print('Race: ' + pc.race)
                    self.print_creature(pc)
                    found = True
        
        if not found:
            raise ValueError('Unknown element ' + element_name)
