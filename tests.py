import unittest
from datetime import date
import models

rates = {
    'bus': {'single_ride': 6.00, 'monthly': 60.00},
    'subway': {'single_ride': 4.00, 'monthly': 40.00},
    'rail': {'single_ride': 5.00, 'monthly': 50.00},
    'seniorbus': {'single_ride': 2.00, 'monthly': 20.00}
}
discounts = {
    'customer': {'adult': 1.0, 'student':0.50, 'senior':0.50, 'employee':0.0},
    'length': 0.10
}

class TestMonthlyPasses(unittest.TestCase):
    def SetUp(self):
        self.rates = rates
        self.discounts = discounts
        self.ticket = models.Ticket(type='unlimited', mode='bus', purchase_date=date(2013,5,1))
        self.cust = models.Customer(type='senior', ticket=self.ticket)
    def test_take_ride(self):
        ride = models.Ride('bus', date(2013, 5, 23))
        self.machine.swipePass(self.cust, ride)
        self.assertEqual(42.50, self.cust.ticket.balance)
    def test_purchase_ticket(self):
        machine.dispensePass(self.cust, self.ticket)
        self.assertEqual(30.00, ticket.monthly_price)

class TestBalancePasses(unittest.TestCase):
    """Tests for passes with a balance loaded onto them"""
    def SetUp(self):
        self.rates = rates
        self.discounts = discounts
        machine = models.VendingMachine(self.rates, self.discounts)
        ticket = models.Ticket(type='balance', purchase_date=date(2013,5,1), balance=45.00)
        cust = models.Customer(type='senior', ticket=ticket)
    def test_take_ride(self):
        """Test that ticket balance is adjusted properly when taking a ride"""
        machine = models.VendingMachine(self.rates, self.discounts)
        ride = models.Ride('rail', date(2013, 5, 23))
        machine.swipePass(self.cust, ride)
        self.assertEqual(42.50, self.cust.ticket.balance)

if __name__ == '__main__':
    unittest.main()
