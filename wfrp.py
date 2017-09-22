import json
import random
import sys


def to_data_array(array):
    data_array = []
    for element in array:
        data_array.append(element.to_data())

    return data_array

 
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

    @property
    def creatures(self):
        return self._creatures

    def add_creature(self, creature):
        self._creatures.append(creature)

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
        except FileNotFoundError:
            return Wfrp()   


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
        campaign = Campaign(data['name'])
        for element in data['party']:
            pc = Character.from_data(element)
            campaign.add_player_character(pc)

        return campaign


class Creature(object):
    def __init__(self, name, weapon_skill, ballistic_skill, strength, toughness, agility, intelligence, willpower, fellowship, wounds):
        self._name = name
        self._weapon_skill = weapon_skill
        self._ballistic_skill = ballistic_skill
        self._strength = strength
        self._toughness = toughness
        self._agility = agility
        self._intelligence = intelligence
        self._willpower = willpower
        self._fellowship = fellowship
        self._wounds = wounds

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
            'wounds': self.wounds
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
            data['wounds'])


class Character(Creature):
    def __init__(self, name, race, weapon_skill, ballistic_skill, strength, toughness, agility, intelligence, willpower, fellowship, wounds):
        self._race = race
        super(Character, self).__init__(name, weapon_skill, ballistic_skill, strength, toughness, agility, intelligence, willpower, fellowship, wounds)

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
            creature.wounds)
