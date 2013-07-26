from datetime import date

# these should probably be in a data file or database instead of hardcoded
ride_rates = {'bus':6.00, 'subway':4.00, 'rail':5.00, 'seniorbus':2.00}
monthly_rates = {'bus':60.00, 'subway':40.00, 'rail':50.00, 'seniorbus':20.00}
discounts = {'regular': 1.0, 'student':0.50, 'senior':0.50, 'employee':0.0}

class Customer(object):
    def __init__(self, type, ticket):
        if isinstance(ticket, Ticket):
            self.ticket = ticket
        else:
            raise TypeError
        if type in discounts:
            self.type = type
        else:
            raise ValueError("Bad customer type value: " + type)
    def takeRide(self, ride, date):
        if not isinstance(ride, Transport):
            raise TypeError
        if self.ticket.type == 'balance':
            self.ticket.balance = (self.ticket.balance - (ride.fee * discounts[self.type]))
            return self.ticket.balance
        if self.ticket.type == 'unlimited' and self.ticket.mode != ride.type:
            raise ValueError("Customer cannot use this type of ticket on this ride!")

class Ticket(object):
    def __init__(self, type, purchase_date, mode=None, balance=0.00):
        self.type = type
        self.mode = mode
        self.purchase_date = purchase_date
        if self.type == 'balance':
            self.balance = balance
        if self.type == 'unlimited':
            self.monthly_price = self.calculateMonthlyPrice()
    def calculateMonthlyPrice(self):
        self.monthly_price = monthly_rates[self.mode]
        day_purchased = self.purchase_date.day
        if day_purchased > 15:
            return self.monthly_price * 0.50
        else:
            return self.monthly_price


class Transport(object):
    def __init__(self, type):
        if type in ride_rates:
            self.type = type
        else:
            raise ValueError
        self.time = date
        self.fee = ride_rates[self.type]

class VendingMachine(object):
    def dispensePass(self, customer, ticket):
        pass

class SwipeMachine(object):
    def swipePass(self, customer):
        pass
