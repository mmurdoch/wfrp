import unittest

from wfrp import *


class CommandExecutorTest(unittest.TestCase):

    def test_execute_unknown_command(self):
        command_executor = CommandExecutor()

        try:
            command_executor.execute_command(['unknown'])
            self.fail()
        except ValueError:
            pass

 
if __name__ == '__main__':
    unittest.main()
