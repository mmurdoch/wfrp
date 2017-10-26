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
        print('  Armour:          ' + str(creature.armour))

    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing element name')

        element_name = command_parts[0]

        found = False
        creature = wfrp.find_creature(element_name)
        if creature:
            print('Name: ' + creature.name + ' (creature)')
            self.print_creature(creature)
            found = True

        campaign = wfrp.find_campaign(element_name)
        if campaign:
            print('Name: ' + campaign.name + ' (campaign)')
            print('Current encounter is: ' + campaign.current_encounter.name)
            print('Encounters:')
            for encounter in campaign.encounters:
                encounter_state = ''
                if campaign.current_encounter == encounter:
                    encounter_state = ' (current)' 
                print('  Name: ' + encounter.name + encounter_state)
                print('  Creatures:')
                for i in range(len(encounter.creatures)):
                    creature = encounter.creatures[i]
                    creature_state = ''
                    if creature.wounds <= 0:
                        creature_state = ' (deceased)'
                    print('    Type: ' + creature.name + ', ID: ' + str(i) + creature_state)
 
                found = True

        for campaign in wfrp.campaigns:
            pc = campaign.find_player_character(element_name)
            if pc:
                print('Name: ' + pc.name + ' (player character)')
                print('Race: ' + pc.race)
                self.print_creature(pc)
                found = True
        
        if not found:
            raise ValueError('Unknown element ' + element_name)
