import unittest

from generatecommand import *


class GenerateCommandTest(unittest.TestCase):

    def test_generate_pc_with_no_campaign(self):
        command = GenerateCommand()

        try:
            command.execute(Wfrp(), ['human'])
            self.fail()
        except ValueError:
            pass

    def test_generate_with_no_race_fails(self):
        wfrp = Wfrp()
        wfrp.add_campaign(Campaign('Arbitrary Name'))
        command = GenerateCommand()

        try:
            command.execute(wfrp, [])
            self.fail()
        except ValueError:
            pass

    def test_generate_random_pc(self):
        wfrp = Wfrp()
        wfrp.add_campaign(Campaign('Arbitrary Name'))
        command = GenerateCommand()

        command.execute(wfrp, ['random'])

        self.assertEqual(1, len(wfrp.current_campaign.party))

    def test_generate_human_pc(self):
        self.check_generate_pc_with_supported_race('human')

    def test_generate_elf_pc(self):
        self.check_generate_pc_with_supported_race('elf') 

    def test_generate_invalid_race_pc(self):
        try:
            self.generate_pc_with_race(Wfrp(), 'not a race')
            self.fail()
        except ValueError:
            pass

    def check_generate_pc_with_supported_race(self, race):
        wfrp = Wfrp()
        self.generate_pc_with_race(wfrp, race) 

        self.assertEqual(race, wfrp.current_campaign.party[0].race)

    def generate_pc_with_race(self, wfrp, race):
        wfrp.add_campaign(Campaign('Arbitrary Campaign'))
        command = GenerateCommand()

        command.execute(wfrp, [race])


if __name__ == '__main__':
    unittest.main()
