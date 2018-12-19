import unittest
import game
import databaseSetup


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        databaseSetup.setup()
        game.setupPlayers(4)

    def test_changeAccount2(self):
        game.updateAccountBalance(1, -200)
        self.assertEqual(game.getAccountBalance(1), 1300)

    def test_changeAccount(self):
        prev = game.getAccountBalance(1)
        game.updateAccountBalance(1, -200)
        curr = game.getAccountBalance(1)
        self.assertEqual(prev - 200, curr)

    def test_getRent(self):
        self.assertEqual(game.getRent(3), 4)

    def test_owner(self):
        self.assertEqual(game.getOwner(3), 0)

    def test_changeOwner(self):
        game.changeOwner(3, 2)
        self.assertEqual(game.getOwner(3), 2)

    def test_buy(self):
        game.buy(7, 3)
        self.assertEqual(game.getAccountBalance(3), 1500 - 120)
        self.assertEqual(game.getOwner(7), 3)

    def test_pay(self):
        game.pay(6, 2, 3)
        self.assertEqual(game.getAccountBalance(2), 1494)
        self.assertEqual(game.getAccountBalance(3), 1506)


if __name__ == '__main__':
    unittest.main(exit=False)
