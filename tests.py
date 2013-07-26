import unittest
from datetime import date
import models

class TransportationTest(unittest.TestCase):
    def SetUp(self):
        # not sure what to put here?
        pass
    def test_new_customer(self):
        """Make sure customer cannot be initialized with bogus type value"""
        ticket = models.Ticket(type='balance', purchase_date=date(2013,5,1), mode='bus', balance=45.00)
        # kind of sucks that Customer cannot be tested on its own
        with self.assertRaises(ValueError): models.Customer(type='foo', ticket=ticket)
    def test_take_ride(self):
        """Test that ticket balance is adjusted properly when taking a ride"""
        cust = models.Customer(type='senior', ticket=models.Ticket('unlimited', 'bus', date(2013,5,1), 45.00))
        ride = models.Transport('rail')
        # should takeRide be a method of Customer?
        cust.takeRide(ride, date(2013, 5, 23))
        self.assertEqual(42.50, cust.ticket.balance)
    def test_purchase_ticket(self):
        ticket = models.Ticket('unlimited', 'subway', date(2013,5,25))
        self.assertEqual(20.00, ticket.monthly_price)

if __name__ == '__main__':
    unittest.main()
