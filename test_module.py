import unittest
import budget
from budget import create_spend_chart


class UnitTests(unittest.TestCase):

  def setUp(self):
    self.food = budget.Category("Food")
    self.clothing = budget.Category("Clothing")
    self.auto = budget.Category("Auto")

  def test_deposit(self):
    self.food.deposit(1000, "initial deposit")
    actual = self.food.ledger[0]
    expected = {"amount": 1000, "description": "initial deposit"}
    self.assertEqual(
      actual, expected,
      'Expected `deposit` method to create a specific object in the ledger instance variable.'
    )

  def test_deposit_no_description(self):
    self.food.deposit(500)
    actual = self.food.ledger[0]
    expected = {"amount": 500, "description": ""}
    self.assertEqual(
      actual, expected,
      'Expected calling `deposit` method with no description to create a blank description.'
    )

  def test_withdraw(self):
    self.food.deposit(100, "initial deposit")
    self.food.withdraw(12, "restaurant")
    actual = self.food.ledger[1]
    expected = {"amount": -12, "description": "restaurant"}
    self.assertEqual(
      actual, expected,
      'Expected `withdraw` method to create a specific object in the ledger instance variable.'
    )

  def test_withdraw_no_description(self):
    self.food.deposit(250, "initial deposit")
    good_withdraw = self.food.withdraw(15.15)
    actual = self.food.ledger[1]
    expected = {"amount": -15.15, "description": ""}
    self.assertEqual(
      actual, expected,
      'Expected `withdraw` method with no description to create a blank description.'
    )
    self.assertEqual(good_withdraw, True,
                     'Expected `transfer` method to return `True`.')

  def test_get_balance(self):
    self.food.deposit(100, "deposit")
    self.food.withdraw(12.90, "restaurant")
    actual = self.food.get_balance()
    expected = 87.10
    self.assertEqual(actual, expected, 'Expected balance to be 87.10')

  def test_transfer(self):
    self.food.deposit(100, "deposit")
    self.food.withdraw(12.90, "restaurant")
    good_transfer = self.food.transfer(25, self.clothing)
    actual = self.food.ledger[2]
    expected = {"amount": -25, "description": "Transfer to Clothing"}
    self.assertEqual(
      actual, expected,
      'Expected `transfer` method to create a specific ledger item in food object.'
    )
    self.assertEqual(good_transfer, True,
                     'Expected `transfer` method to return `True`.')
    actual = self.clothing.ledger[0]
    expected = {"amount": 25, "description": "Transfer from Food"}
    self.assertEqual(
      actual, expected,
      'Expected `transfer` method to create a specific ledger item in clothing object.'
    )

  def test_check_funds(self):
    self.food.deposit(10, "deposit")
    actual = self.food.check_funds(25)
    expected = False
    self.assertEqual(actual, expected,
                     'Expected `check_funds` method to be False')
    actual = self.food.check_funds(10)
    expected = True
    self.assertEqual(actual, expected,
                     'Expected `check_funds` method to be True')

  def test_withdraw_no_funds(self):
    self.food.deposit(100, "deposit")
    good_withdraw = self.food.withdraw(200)
    self.assertEqual(good_withdraw, False,
                     'Expected `withdraw` method to return `False`.')

  def test_transfer_no_funds(self):
    self.food.deposit(100, "deposit")
    good_transfer = self.food.transfer(150, self.clothing)
    self.assertEqual(good_transfer, False,
                     'Expected `transfer` method to return `False`.')

  def test_to_string(self):
    self.food.deposit(100, "initial deposit")
    self.food.withdraw(12.90, "restaurant")
    self.food.transfer(25, self.clothing)
    actual = str(self.food)
    expected = f"*************Food*************\ninitial deposit         100.00\nrestaurant              -12.90\nTransfer to Clothing    -25.00\nTotal: 62.10"
    self.assertEqual(actual, expected,
                     'Expected different string representation of object.')

  def test_create_spend_chart(self):
    self.food.deposit(500, "initial deposit")
    self.clothing.deposit(500, "initial deposit")
    self.auto.deposit(500, "initial deposit")
    self.food.withdraw(100.20)
    self.clothing.withdraw(55.50)
    self.auto.withdraw(20)
    actual = create_spend_chart([self.auto, self.food, self.clothing])
    expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|          \n 60|          \n 50|    o     \n 40|    o     \n 30|    o  o  \n 20|    o  o  \n 10| o  o  o  \n  0| o  o  o  \n    ----------\n     A  F  C  \n     u  o  l  \n     t  o  o  \n     o  d  t  \n           h  \n           i  \n           n  \n           g  "
    self.assertEqual(
      actual, expected,
      'Expected different chart representation. Check that all spacing is exact.'
    )


if __name__ == "__main__":
  unittest.main()
