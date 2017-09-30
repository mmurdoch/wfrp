import unittest

from addcommand import *
from wfrp import *


class AddCommandTest(unittest.TestCase):

    def test_add_no_element_fails(self):
        command = AddCommand()

        try:
            command.execute(Wfrp(), [])
            self.fail()
        except ValueError as e:
            pass

    def test_add_campaign(self):
        wfrp = Wfrp()
        command = AddCommand()

        name = 'arbitrary name'
        command.execute(wfrp, ['campaign', name])

        self.assertEqual(name, wfrp.campaigns[0].name)

    def test_add_campaign_without_name_fails(self):
        command = AddCommand()

        try:
            command.execute(Wfrp(), ['campaign'])
            self.fail()
        except ValueError:
            pass 

    def test_add_creature(self):
        wfrp = Wfrp()
        command = AddCommand()

        name = 'Arbitrary name'
        command.execute(wfrp, ['creature', name, '1', '2','3','4','5','6','7','8','9', '10', '11'])

        creature = wfrp.creatures[0]
        self.assertEqual(name, creature.name)
        self.assertEqual(1, creature.weapon_skill)
        self.assertEqual(2, creature.ballistic_skill)
        self.assertEqual(3, creature.strength)
        self.assertEqual(4, creature.toughness)
        self.assertEqual(5, creature.agility)
        self.assertEqual(6, creature.intelligence)
        self.assertEqual(7, creature.willpower)
        self.assertEqual(8, creature.fellowship)
        self.assertEqual(9, creature.wounds)

    def test_add_pc(self):
        wfrp = Wfrp()
        wfrp.add_campaign(Campaign('Arbitrary Name'))
        command = AddCommand()

        name = 'Arbitrary name'
        command.execute(wfrp, ['pc', name, 'random', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

        pc = wfrp.current_campaign.party[0]
        self.assertEqual(name, pc.name)
        self.assertEqual(1, pc.weapon_skill)
        self.assertEqual(2, pc.ballistic_skill)
        self.assertEqual(3, pc.strength)
        self.assertEqual(4, pc.toughness)
        self.assertEqual(5, pc.agility)
        self.assertEqual(6, pc.intelligence)
        self.assertEqual(7, pc.willpower)
        self.assertEqual(8, pc.fellowship)
        self.assertEqual(9, pc.wounds)

    def test_add_encounter(self):
        wfrp = Wfrp()
        wfrp.add_campaign(Campaign('Arbitrary Name'))
        creature = Creature('Mutant', 31, 31, 31, 31, 31, 31, 31, 31, 11, 1, 0)
        wfrp.add_creature(creature)
        command = AddCommand()

        name = 'Mutant Attack!'
        command.execute(wfrp, ['encounter', name, creature.name, creature.name])

        encounter = wfrp.current_campaign.encounters[0]
        self.assertEqual(name, encounter.name)
        self.assertEqual(creature.name, encounter.creatures[0].name)
        self.assertEqual(creature.name, encounter.creatures[1].name)

    def test_add_invalid_element_fails(self):
        command = AddCommand()

        try:
            command.execute(Wfrp(), ['invalid', 'arbitrary name'])
            self.fail()
        except ValueError:
            pass

 
if __name__ == '__main__':
    unittest.main()
