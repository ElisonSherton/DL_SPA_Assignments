# Subscribe to both topics order buy and order sell
# Run the logic to create match and execute transactions

import random, pickle
from datetime import datetime, timedelta
from order_generation_utils import *
random.seed(42)
from collections import Counter
import pandas as pd

ORDER_INFO = "order_info.pkl"

def read_orders(orders_pth):
    order_data = pickle.load(open(ORDER_INFO, "rb"))

    # Get a list of all the instruments and print some basic stats
    

    

read_orders(ORDER_INFO)



