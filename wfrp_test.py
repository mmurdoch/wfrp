import unittest

from wfrp import *


class AddTest(unittest.TestCase):

    def setUp(self):
        self.wfrp = Wfrp()

    def test_add_campaign(self):
        command = ['add', 'campaign', 'Paths of the Damned']
        self.execute_command(command)
 
        self.assertEqual(1, len(self.wfrp.campaigns))
        self.assertEqual('Paths of the Damned', self.wfrp.campaigns[0].name)

    def test_generate_pc_with_no_campaign(self):
        command = ['generate', 'pc', 'human']
        try:
            self.execute_command(command)
            self.fail()
        except ValueError:
            pass

    def test_generate_human_pc(self):
        self.check_generate_pc_with_supported_race('human')

    def test_generate_elf_pc(self):
        self.check_generate_pc_with_supported_race('elf') 

    def test_generate_invalid_race_pc(self):
        try:
            self.generate_pc_with_race('not a race')
            self.fail()
        except ValueError:
            pass

    def check_generate_pc_with_supported_race(self, race):
        self.generate_pc_with_race(race) 

        self.assertEqual(race, self.wfrp.current_campaign.party[0].race)

    def generate_pc_with_race(self, race):
        self.wfrp.add_campaign('Arbitrary Campaign')

        command = ['generate', 'pc', race]
        self.execute_command(command)

    def execute_command(self, command):
        self.wfrp.execute_command(command)


if __name__ == '__main__':
    unittest.main()
