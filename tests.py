import unittest, json
from datetime import date
import models

class TransportTest(unittest.TestCase):
    def setUp(self):
        self.data = json.load(open('test_data.json'))
        self.machine = models.VendingMachine(self.data)

class TestMonthlyPasses(TransportTest):
    """Tests for monthly unlimited passes"""
    def test_expired_pass(self):
        ticket = models.MonthlyPass(mode='bus', purchase_date=date(2013,5,1))
        ride = models.Ride('bus', date(2013, 6, 2))
        with self.assertRaises(models.InvalidPassError): self.machine.swipePass(ticket, ride)
    def test_invalid_transport_mode(self):
        ticket = models.MonthlyPass('subway', date(2013,5,1))
        ride = models.Ride('bus', date(2013,5,23))
        with self.assertRaises(models.InvalidPassError): self.machine.swipePass(ticket, ride)
    def test_pro_rated_discount(self):
        ticket = models.MonthlyPass(mode='bus', purchase_date=date(2013,5,23))
        self.machine.dispensePass(ticket)
        self.assertEqual(30.00, ticket.price)
    def test_add_money_to_monthly_pass(self):
        ticket = models.MonthlyPass(mode='bus', purchase_date=date(2013,5,1))
        with self.assertRaises(AttributeError): self.machine.addMoneyToPass(ticket, 5.00)

class TestBalancePasses(TransportTest):
    """Tests for passes with a balance loaded onto them"""
    def test_senior_discount(self):
        """Test that ticket balance is adjusted properly when taking a ride"""
        ticket = models.BalancePass(balance=45.0, customer_type='senior')
        ride = models.Ride('rail', date(2013, 5, 23))
        self.machine.swipePass(ticket, ride)
        self.assertEqual(42.50, ticket.balance)
    def test_weekend_discount(self):
        ticket = models.BalancePass(balance=45.0)
        ride = models.Ride('rail', date(2013, 7, 28))
        self.machine.swipePass(ticket, ride)
        self.assertEqual(41.25, ticket.balance)
    def test_weekend_and_senior_discount(self):
        ticket = models.BalancePass(balance=45.0, customer_type='senior')
        ride = models.Ride('rail', date(2013, 7, 28))
        self.assertEqual(43.125, ticket.balance)

if __name__ == '__main__':
    unittest.main()
