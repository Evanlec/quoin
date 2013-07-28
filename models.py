from datetime import date

class Customer(object):
    def __init__(self, type, ticket):
        self.ticket = ticket
        self.type = type
    def takeRide(self, ride, date):
        if self.ticket.type == 'balance':
            self.ticket.balance = (self.ticket.balance - (ride.fee * discounts[self.type]))
            return self.ticket.balance
        elif self.ticket.type == 'unlimited' and self.ticket.mode != ride.type:
            raise ValueError("Customer cannot use this type of ticket on this ride!")
        else:
            raise ValueError("Bad customer type value: " + type)

class Ticket(object):
    def __init__(self, type, purchase_date, mode=None, balance=0.00):
        self.type = type
        self.mode = mode
        self.purchase_date = purchase_date
        self.balance = balance
    def adjustBalance(self, amount):
        if (self.balance + amount) < 0:
            print('Error: ticket balance less than zero') 
        else:
            self.balance = (self.balance + amount)

class Ride(object):
    def __init__(self, mode, date, ride_length=0):
        self.mode = mode
        self.date = date
        self.ride_length = ride_length

class VendingMachine(object):
    """Vending Machine class contains all relevant 'actions' for the system, and is initialized with
    rates/discount values, contains most of all business logic"""
    def __init__(self, rates, discounts):
        self.rates = rates
        self.discounts = discounts

    def dispensePass(self, customer, ticket, balance=0.00):
        if ticket.type == 'balance':
            ticket.balance = balance
            customer.ticket = ticket
            return "Customer purchased normal pass with starting balance of: %d" % ticket.balance
        if ticket.type == 'unlimited':
            base_price = self.rates[ticket.mode]['monthly']
            day_purchased = ticket.purchase_date.day
            if day_purchased > 15:
                ticket.monthly_price = base_price * 0.50
            else:
                ticket.monthly_price = base_price
            customer.ticket = ticket

    def addMoneyToPass(self, ticket, amount):
        if ticket.type == 'unlimited':
            raise ValueError('Cannot add money to monthly pass type')
        ticket.balance += amount
        return "New ticket balance: %d" % ticket.balance

    def swipePass(self, customer, ride):
        """pass is swiped when customer takes a ride"""
        if customer.ticket.type == 'balance':
            customer.ticket.adjustBalance(-1 * self.getSingleRidePrice(customer, ride))
            return customer.ticket.balance
        if customer.ticket.type == 'unlimited':
            if customer.ticket.mode != ride.mode:
                return "Error: Customer cannot use this type of ticket for this ride!"

    def checkBalance(self, ticket):
        return ticket.balance

    def getSingleRidePrice(self, customer, ride):
        # customer type discount
        fee = (self.rates[ride.mode] * self.discounts['customer'][customer.type])
        # weekend discount
        if ride.date.weekday() > 4:
            fee = fee * 0.75
        if ride.length > 0:
            fee = fee * (1 - (self.discounts['length'] * length))

        return fee

    def calculateMonthlyPrice(self):
        self.monthly_price = transports[self.mode]['monthly']
        day_purchased = self.purchase_date.day
        if day_purchased > 15:
            return self.monthly_price * 0.50
        else:
            return self.monthly_price
