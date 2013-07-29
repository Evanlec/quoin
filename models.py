from datetime import date

class InvalidPassError(Exception):
    """Exception raised when a pass is swiped and user shall not be allowed further"""
    pass

class Pass(object):
    def __init__(self, customer_type):
        self.customer_type = customer_type

class BalancePass(Pass):
    def __init__(self, balance=0.0, customer_type='adult'):
        super(BalancePass, self).__init__(customer_type)
        self.balance = balance
    def adjustBalance(self, amount):
        if (self.balance + amount) < 0:
            raise InvalidPassError('ticket balance less than zero') 
        else:
            self.balance = (self.balance + amount)

class MonthlyPass(Pass):
    def __init__(self, mode, purchase_date, customer_type='adult'):
        super(MonthlyPass, self).__init__(customer_type)
        self.mode = mode
        self.purchase_date = purchase_date

class Ride(object):
    def __init__(self, mode, date, ride_length=0):
        self.mode = mode
        self.date = date
        self.ride_length = ride_length

class VendingMachine(object):
    """Vending Machine class contains all relevant 'actions' for the system, and is initialized with
    rates/discount values, contains most of all business logic"""
    def __init__(self, data):
        self.rates = data['rates']
        self.discounts = data['discounts']

    def dispensePass(self, ticket, balance=0.00):
        if hasattr(ticket, 'balance'):
            ticket.balance = balance
            return "Customer purchased normal pass with starting balance of: %d" % ticket.balance
        if hasattr(ticket, 'mode'):
            base_price = self.rates[ticket.mode]['monthly']
            day_purchased = ticket.purchase_date.day
            if day_purchased > 15:
                ticket.monthly_price = base_price * 0.50
            else:
                ticket.monthly_price = base_price

    def addMoneyToPass(self, ticket, amount):
        ticket.adjustBalance(amount)
        return "New ticket balance: %d" % ticket.balance

    def swipePass(self, ticket, ride):
        """pass is swiped when customer takes a ride"""
        if hasattr(ticket, 'balance'):
            ticket.adjustBalance(-1 * self.getSingleRidePrice(ticket, ride))
            return ticket.balance
        if hasattr(ticket, 'mode'):
            if ticket.mode != ride.mode:
                raise InvalidPassError("Customer cannot use this type of ticket for this ride!")

    def checkBalance(self, ticket):
        return ticket.balance

    def getSingleRidePrice(self, ticket, ride):
        # customer type discount
        fee = (self.rates[ride.mode]['single_ride'] * self.discounts['customer'][ticket.customer_type])
        # weekend discount
        if ride.date.weekday() > 4:
            fee = fee * 0.75
        if ride.ride_length > 0:
            fee = fee * (1 - (self.discounts['length'] * ride.ride_length))
        return fee

    def calculateMonthlyPrice(self):
        self.monthly_price = transports[self.mode]['monthly']
        day_purchased = self.purchase_date.day
        if day_purchased > 15:
            return self.monthly_price * 0.50
        else:
            return self.monthly_price
