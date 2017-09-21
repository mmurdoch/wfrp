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

    def test_add_invalid_element_fails(self):
        command = AddCommand()

        try:
            command.execute(Wfrp(), ['invalid', 'arbitrary name'])
            self.fail()
        except ValueError:
            pass

 
if __name__ == '__main__':
    unittest.main()
