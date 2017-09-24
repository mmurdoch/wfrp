from __future__ import print_function
from command import *
from wfrp import *


def get_pc_roll(purpose, die_sides):
    while True:
        try:
            print('Enter ' + purpose + ' roll (d' + str(die_sides) + '): ', end='')
            roll = int(raw_input())
            if roll > 0 and roll <= die_sides:
                return roll
        except ValueError:
            pass 

def get_pc_attack_roll():
    return get_pc_roll('attack', 100)


def pc_attack_hit():
    print('Hit!')


def pc_attack_miss():
    print('Missed')


def pc_attack():
    return {
        'roll': get_pc_attack_roll,
        'hit': pc_attack_hit,
        'miss': pc_attack_miss }


def get_pc_damage_roll():
    return get_pc_roll('damage', 10)


def pc_damage_done(damage):
    print('Inflicted ' + str(damage) + ' damage')


def pc_damage_none():
    print('Deflected, no damage')


def pc_damage():
    return {
        'roll': get_pc_damage_roll,
        'done': pc_damage_done,
        'none': pc_damage_none } 


def get_creature_attack_roll():
    return d100()


def creature_attack_hit():
    print('Hit!')


def creature_attack_miss():
    print('Missed')


def creature_attack():
    return {
        'roll': get_creature_attack_roll,
        'hit': creature_attack_hit,
        'miss': creature_attack_miss }


def get_creature_damage_roll():
    return d10()


def creature_damage_done(damage):
    print('Inflicted ' + str(damage) + ' damage')


def creature_damage_done():
    print('Deflected, no damage')


def creature_damage():
    return {
        'roll': get_creature_attack_roll,
        'hit': creature_attack_hit,
        'miss': creature_attack_miss }


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

            return creature
        except ValueError:
            raise ValueError('Invalid creature ID ' + id)

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

        pc = wfrp.current_campaign.find_player_character(attacker)
        if pc:
            creature = self.find_creature(wfrp, defender)
            print(pc.name + ' attacking ' + creature.name + '#' + defender)
            wfrp.current_encounter.attack(pc, creature, pc_attack(), pc_damage())
        else:
            creature = self.find_creature(wfrp, attacker)
            pc = self.find_player_character(wfrp, defender)
            print(creature.name + '#' + attacker + ' attacking ' + pc.name)
            wfrp.current_encounter.attack(creature, pc, creature_attack(), creature_damage())
