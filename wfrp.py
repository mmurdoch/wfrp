#!/usr/bin/python

import random

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
 
