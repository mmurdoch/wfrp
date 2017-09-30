import json
import random
import sys


def to_data_array(array):
    data_array = []
    for element in array:
        data_array.append(element.to_data())

    return data_array


def find_element(elements, name_start):
    matching_elements = []

    for element in elements:
        if element.name.startswith(name_start):
            matching_elements.append(element)

    if len(matching_elements) == 1:
        return matching_elements[0]

    return None        


def roll_die(sides):
    return random.randint(1, sides)


def roll_d100():
    return roll_die(100)


def roll_d10():
    return roll_die(10)

 
class Wfrp(object):
    def __init__(self):
        self._campaigns = []
        self._current_campaign = None
        self._creatures = []

    @property
    def campaigns(self):
        return self._campaigns

    @property
    def current_campaign(self):
        return self._current_campaign

    def add_campaign(self, campaign):
        self._campaigns.append(campaign)
        self._current_campaign = campaign 

    def find_campaign(self, name_start):
        return find_element(self.campaigns, name_start)

    @property
    def current_encounter(self):
        if self.current_campaign:
            return self.current_campaign.current_encounter

        return None

    @property
    def creatures(self):
        return self._creatures

    def add_creature(self, creature):
        self._creatures.append(creature)

    def find_creature(self, name_start):
        return find_element(self.creatures, name_start)

    @property
    def supported_pc_races(self):
        return ['dwarf', 'elf', 'halfling', 'human']

    def random_pc_race(self):
        return self.supported_pc_races[
            random.randint(0, len(self.supported_pc_races)-1)]

    def to_data(self):
        return {
            'campaigns': to_data_array(self._campaigns),
            'creatures': to_data_array(self._creatures) 
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

        for element in data['creatures']:
            creature = Creature.from_data(element)
            wfrp.add_creature(creature)

        return wfrp 

    @staticmethod
    def load():
        try:
            with open('wfrp.json', 'r') as data_file:
                file_content = data_file.read()
                data = json.loads(file_content)
                return Wfrp.from_data(data)
        except IOError:
            return Wfrp()   


class Campaign(object):
    def __init__(self, name):
        self._name = name
        self._party = []
        self._encounters = []
        self._current_encounter = None

    @property
    def name(self):
       return self._name

    def add_player_character(self, character):
        self._party.append(character) 

    @property
    def party(self):
       return self._party 

    def find_player_character(self, name_start):
        return find_element(self.party, name_start)

    def add_encounter(self, encounter):
        self._encounters.append(encounter)
        self._current_encounter = self.encounters[0]

    @property
    def encounters(self):
        return self._encounters

    @property
    def current_encounter(self):
        return self._current_encounter

    @current_encounter.setter
    def current_encounter(self, value):
        self._current_encounter = value

    def find_encounter(self, name_start):
        return find_element(self.encounters, name_start)

    def to_data(self):
        data = {
            'name': self._name,
            'party': to_data_array(self.party),
            'encounters': to_data_array(self.encounters)
        }

        if self.current_encounter:
            data['current_encounter'] = self.current_encounter.name

        return data

    @staticmethod
    def from_data(data):
        campaign = Campaign(data['name'])

        for element in data['party']:
            pc = Character.from_data(element)
            campaign.add_player_character(pc)

        for element in data['encounters']:
            encounter = Encounter.from_data(element)
            campaign.add_encounter(encounter) 

        if 'current_encounter' in data:
            campaign.current_encounter = campaign.find_encounter(data['current_encounter'])

        return campaign


class Encounter(object):
    def __init__(self, name, *args):
        self._name = name
        self._creatures = list(args)

    @property
    def name(self):
        return self._name

    @property
    def creatures(self):
        return self._creatures

    def find_creature(self, id):
        if id >= 0 and id < len(self.creatures):
            return self.creatures[id]

        return None 

    def first_attack_roll_damage(self, damage):
        return damage['roll']()

    def ulriks_fury_roll_damage(self, damage):
        damage_roll = 0
        continue_rolling_damage = True
        while continue_rolling_damage:
            further_damage_roll = damage['roll']()
            damage_roll += further_damage_roll
            if further_damage_roll != 10: 
                continue_rolling_damage = False

        return damage_roll

    def make_attack(self, attacker, attack, damage, roll_damage):
        attack_roll = attack['roll']()
        if attack_roll <= attacker.weapon_skill:
            attack['hit']()
            return roll_damage(damage)
        else:
            attack['miss']()
            return 0
    
    def attack(self, attacker, defender, attack, damage):
        damage_roll = self.make_attack(attacker, attack, damage, self.first_attack_roll_damage)
        if damage_roll == 10:
            damage_roll += self.make_attack(attacker, attack, damage, self.ulriks_fury_roll_damage)

        if damage_roll > 0:
            damage['weapon'](attacker.name, attacker.weapon_damage)
            damage['toughness'](defender.name, defender.toughness_bonus)
            damage['armour'](defender.name, defender.armour)
            total_damage = damage_roll + attacker.weapon_damage - defender.toughness_bonus - defender.armour
            if total_damage > 0:
                damage['done'](total_damage)
                defender.wounds -= total_damage
            else:
                damage['none']()

    def to_data(self):
        return {
            'name': self.name,
            'creatures': to_data_array(self._creatures)
        }

    @staticmethod
    def from_data(data):
        creatures = []

        for element in data['creatures']:
            creature = Creature.from_data(element)
            creatures.append(creature)

        return Encounter(data['name'], *creatures)


class Creature(object):
    def __init__(self, name, weapon_skill, ballistic_skill, strength, toughness, agility, intelligence, willpower, fellowship, wounds, armour):
        self._name = name
        self._weapon_skill = weapon_skill
        self._ballistic_skill = ballistic_skill
        self._strength = strength
        self._toughness = toughness
        self._agility = agility
        self._intelligence = intelligence
        self._willpower = willpower
        self._fellowship = fellowship
        self._original_wounds = wounds
        self._wounds = wounds
        self._armour = armour

    @property
    def name(self):
        return self._name

    @property
    def weapon_skill(self):
        return self._weapon_skill

    @property
    def ballistic_skill(self):
        return self._ballistic_skill

    @property
    def strength(self):
        return self._strength

    @property
    def toughness(self):
        return self._toughness

    @property
    def agility(self):
        return self._agility

    @property
    def intelligence(self):
        return self._intelligence

    @property
    def willpower(self):
        return self._willpower

    @property
    def fellowship(self):
        return self._fellowship

    @property
    def wounds(self):
        return self._wounds

    @wounds.setter
    def wounds(self, value):
        self._wounds = value

    @property
    def weapon_damage(self):
        return self.strength_bonus

    @property
    def armour(self):
        return self._armour

    @property
    def strength_bonus(self):
        return self.strength / 10

    @property
    def toughness_bonus(self):
        return self.toughness / 10

    def to_data(self):
        return {
            'name': self.name,
            'weapon_skill': self.weapon_skill,
            'ballistic_skill': self.ballistic_skill,
            'strength': self.strength,
            'toughness': self.toughness,
            'agility': self.agility,
            'intelligence': self.intelligence,
            'willpower': self.willpower,
            'fellowship': self.fellowship,
            'wounds': self.wounds,
            'armour': self.armour
        }

    @staticmethod
    def from_data(data):
        return Creature(
            data['name'],
            data['weapon_skill'],
            data['ballistic_skill'],
            data['strength'],
            data['toughness'],
            data['agility'],
            data['intelligence'],
            data['willpower'],
            data['fellowship'],
            data['wounds'],
            data['armour'])


class Character(Creature):
    def __init__(self, name, race, weapon_skill, ballistic_skill, strength, toughness, agility, intelligence, willpower, fellowship, wounds, armour):
        self._race = race
        super(Character, self).__init__(name, weapon_skill, ballistic_skill, strength, toughness, agility, intelligence, willpower, fellowship, wounds, armour)

    @property
    def race(self):
        return self._race

    def to_data(self):
        data = super(Character, self).to_data()
        data['race'] = self.race

        return data

    @staticmethod
    def from_data(data):
        creature = Creature.from_data(data)

        return Character(
            creature.name,
            data['race'],
            creature.weapon_skill,
            creature.ballistic_skill,
            creature.strength,
            creature.toughness,
            creature.agility,
            creature.intelligence,
            creature.willpower,
            creature.fellowship,
            creature.wounds,
            creature.armour)
