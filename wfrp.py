#!/usr/bin/python

import random

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

    def add_campaign(self, name):
        campaign = Campaign(name)
        self._campaigns.append(campaign)
        self._current_campaign = campaign 

    @property
    def supported_pc_races(self):
        return ['elf', 'human']

    def execute_command(self, command):
        if (command[0] == 'add'):
            self.add_campaign(command[2])
        elif (command[0] == 'generate'):
            if not self.current_campaign:
                raise ValueError('No current campaign')
            else:
                requested_pc_race = command[2]
                if requested_pc_race in self.supported_pc_races: 
                    self.current_campaign.add_player_character(Character(requested_pc_race))
                else:
                    raise ValueError('Unsupported PC race: ' + requested_pc_race)


class Character(object):
    def __init__(self, race):
        self._race = race

    @property
    def race(self):
        return self._race


class Campaign(object):
    def __init__(self, name):
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


pc = {
    'name': 'Bob',
    'weapon_skill': 84,
    'weapon_damage': 3,
    'toughness_bonus': 3,
    'armour': 1,
    'wounds': 10
}

opponent = {
    'name': 'Beastman',
    'weapon_skill': 34,
    'weapon_damage': 3,
    'toughness_bonus': 3,
    'armour': 1,
    'wounds': 10
}

def roll_die(reason, sides):
    result = random.randint(1, sides)
    print(reason + ' roll: ' + str(result) + ' (out of ' + str(sides) + ')')

    return result

def roll_d100(reason):
    return roll_die(reason, 100)

def roll_d10(reason):
    return roll_die(reason, 10)

def roll_attack():
    return roll_d100('Attack')

def roll_damage():
    return roll_d10('Damage')

def check_roll(roll, character, attribute):
    if roll <= character[attribute]:
        return True

    return False

def make_attack(attacker, defender):
    print(attacker['name'] + ' attacking ' + defender['name'])
    attack_roll = roll_attack()

    return check_roll(attack_roll, attacker, 'weapon_skill')

if make_attack(pc, opponent):
    print('Hit!')
    damage_roll = roll_damage()
    if damage_roll == 10:
        if make_attack(pc, opponent):
            print('Ulric\'s Fury!')
            continue_rolling_damage = True
            while continue_rolling_damage:
                further_damage_roll = roll_damage()
                print('Additional damage: ' + str(further_damage_roll))
                damage_roll += further_damage_roll
                if further_damage_roll != 10:
                    continue_rolling_damage = False
    damage = damage_roll + pc['weapon_damage'] - opponent['toughness_bonus'] - opponent['armour'] 
    print('Opponent takes ' + str(damage) + ' damage')
    opponent['wounds'] -= damage
    print('Opponent now has ' + str(opponent['wounds']) + ' wounds')
else:
    print('Miss!')
 
