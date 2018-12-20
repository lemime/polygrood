import unittest
import dbfunctions
import game
import databaseSetup


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        databaseSetup.setup()
        dbfunctions.setupPlayers(4)

    def test_changeAccount2(self):
        dbfunctions.updateAccountBalance(1, -200)
        self.assertEqual(dbfunctions.getAccountBalance(1), 1300)

    def test_changeAccount(self):
        prev = dbfunctions.getAccountBalance(1)
        dbfunctions.updateAccountBalance(1, -200)
        curr = dbfunctions.getAccountBalance(1)
        self.assertEqual(prev - 200, curr)

    def test_getRent(self):
        self.assertEqual(dbfunctions.getRent(3), 4)

    def test_owner(self):
        self.assertEqual(dbfunctions.getOwner(3), 0)

    def test_changeOwner(self):
        dbfunctions.changeOwner(3, 2)
        self.assertEqual(dbfunctions.getOwner(3), 2)

    def test_buy(self):
        game.buy(7, 3)
        self.assertEqual(dbfunctions.getAccountBalance(3), 1500 - 120)
        self.assertEqual(dbfunctions.getOwner(7), 3)

    def test_pay(self):
        game.pay(6, 2, 3)
        self.assertEqual(dbfunctions.getAccountBalance(2), 1494)
        self.assertEqual(dbfunctions.getAccountBalance(3), 1506)


if __name__ == '__main__':
    unittest.main(exit=False)
