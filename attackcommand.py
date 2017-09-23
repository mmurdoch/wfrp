from command import *
from wfrp import *

class AttackCommand(Command):
    def __init__(self):
        super(AttackCommand, self).__init__('attack')

    @property
    def short_help(self):
        return 'Performs an attack'

    @property
    def long_help(self):
        return (
            '  attack <pc_name> <creature_id> <ws_roll> - peforms a melee attack by a player character on a creature in the current encounter with the given weapon skill roll\n' +
            '  attack <creature_id> <pc_name> - performs a melee attack by a creature on a player character in the current encounter')

    def find_creature(self, wfrp, id):
        try:
            id = int(id)
            creature = wfrp.current_campaign.current_encounter.find_creature(id)
            if not creature:
                raise ValueError('Unknown creature ID ' + str(id))
        except ValueError:
            raise ValueError('Invalid creature ID ' + str(id))

    def find_player_character(self, wfrp, name):
        pc = wfrp.current_campaign.find_player_character(name) 
        if not pc:
            raise ValueError('Unknown player character ' + name)

        return pc
    
    def execute(self, wfrp, command_parts):
        if len(command_parts) == 0:
            raise ValueError('Missing attacker')

        if len(command_parts) == 1:
            raise ValueError('Missing defender')

        check_current_encounter(wfrp)

        attacker = command_parts[0]
        defender = command_parts[1]

        if len(command_parts) > 2:
            weapon_skill_roll = int(command_parts[2])
            if weapon_skill_roll < 1 or weapon_skill_roll > 100:
                raise ValueError('Invalid weapon skill roll ' + str(weapon_skill_roll))
            pc = self.find_player_character(wfrp, attacker)
            creature = self.find_creature(wfrp, defender)
            print(pc.name + ' attacking ' + creature.name + '#' + defender)
        else:
            creature = self.find_creature(wfrp, attacker)
            pc = self.find_player_character(wfrp, defender)
            print(creature.name + '#' + attacker + ' attacking ' + pc.name)
