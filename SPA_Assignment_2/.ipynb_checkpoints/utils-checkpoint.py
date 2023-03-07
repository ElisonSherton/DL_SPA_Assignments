import random, json, pickle
from datetime import datetime, timedelta

class Order:
    """
    Define an order object like a struct to store critical information regarding an order 
    """
    def __init__(self, bidder, bid_instrument, bid_price, bid_type,
                 status, bid_time, transaction_time = None):
        super().__init__()
        
        # Name of the person who placed the bid
        self.bidder = bidder
        
        # Which instrument was the bid placed for
        self.bid_instrument = bid_instrument
        
        # What was the price at which the bid was made
        self.bid_price = bid_price
        
        # Was it a buy or a sell bid
        self.bid_type = bid_type
        
        # What time was the bid made
        self.bid_time = bid_time
        
        # What is the status of this bid 
        # 1. Is it active i.e. unmatched
        # 2. Is it inactive i.e. matched with a suitable complementary buy/sell bid
        self.bid_status = status
        
        # What time did the transaction go through
        # i.e. When was this order matched with another order
        self.transaction_time = transaction_time
    
    def __str__(self):
        """
        String representation of the order, when print is called on an instance of Order, 
        this method will be executed. 
        """
        return f"BIDDER: {self.bidder:<8}| INSTRUMENT: {self.bid_instrument:<8}| BID TYPE: {self.bid_type:<4}| BID TIME: {self.bid_time.strftime('%H-%M-%S')}| BID PRICE: {str(self.bid_price):>4} INR| STATUS: {self.bid_status:<8} | TRANSACTION_TIME: {self.transaction_time}"