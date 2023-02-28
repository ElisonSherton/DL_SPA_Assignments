import os, random, json
from pathlib import Path
from collections import namedtuple
from datetime import datetime, timedelta
random.seed(42)

# Read the instruments from the marketplace exchange
# Currently simulating this part from a text file
INSTRUMENTS = json.load(open("data/marketplace_instruments.json", "r"))

# Assume there are three traders currently who're eager to make trades
ENTITIES = ['Vinayak', 'Praveen', 'Shreysi']

# Define the range from which the price of instruments is going to be 
# Sampled in order to place the orders
DISTRIBUTION_PARAMETERS = {'Karza': [10, 20],
                           'Infosys': [1500, 1520],
                           'Rakuten': [390, 420]}

# Define the kinds of bids that can be made
BID_TYPE = ['Buy', 'Sell']

# Define the start time of the trading cycle/day
START_TIME = datetime(2023, 2, 28, 9, 30, 0)

# Limit the volume associated with a particular order
# This is primarily to avoid complication and make understanding easier
BID_VOLUME_HIGH = 5

# When you instantiate an order, the trade hasn't happened yet, hence by default we 
# define the transaction time to be None
DEFAULT_TRANSACTION_TIME = None

class Order:
    def __init__(self, bidder, bid_instrument, bid_price, bid_type,
                 status, bid_time, transaction_time = None):
        super().__init__()
        self.bidder = bidder
        self.bid_instrument = bid_instrument
        self.bid_price = bid_price
        self.bid_type = bid_type
        self.bid_time = bid_time
        self.bid_status = status
        self.transaction_time = transaction_time
    
    def __str__(self):
        return f"BIDDER: {self.bidder:<8}| INSTRUMENT: {self.bid_instrument:<8}| BID TYPE: {self.bid_type:<4}| BID TIME: {self.bid_time.strftime('%H-%M-%S')}| BID PRICE: {str(self.bid_price):>4} INR| STATUS: {self.bid_status:<8} | TRANSACTION_TIME: {self.transaction_time}"

def order_generation():
    orders = []
    for intervals in range(1081):
        bid_volume = random.choice(range(1, BID_VOLUME_HIGH + 1))
        
        bidder = random.choice(ENTITIES)
        bid_time = START_TIME + timedelta(0, 20 * intervals)
        bid_instrument = random.choice(INSTRUMENTS)
        l, u = DISTRIBUTION_PARAMETERS[bid_instrument]
        bid_price = random.choice(range(l, u + 1))
        bid_type = random.choice(BID_TYPE)
        status = "ACTIVE"
        for _ in range(bid_volume):
            o = Order(bidder, bid_instrument, bid_price, bid_type,
                      status, bid_time, DEFAULT_TRANSACTION_TIME)
            orders.append(o)
    return orders


for o in order_generation():
    print(o)