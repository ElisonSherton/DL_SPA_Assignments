from utils import *
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

# Define the end time of the trading cycle/day
END_TIME = datetime(2023, 2, 28, 15, 30, 0)

# Limit the volume associated with a particular order
# This is primarily to avoid complication and make understanding easier
BID_VOLUME_HIGH = 5

# When you instantiate an order, the trade hasn't happened yet, hence by default we 
# define the transaction time to be None
DEFAULT_TRANSACTION_TIME = None

# Define the frequency of order generation
# 1 order every 5 second -> 12 orders per minute -> 12 * 60 orders per hour -> 12 * 60 * 6 hours per working day -> 4320 orders
N_ORDERS = 12 * 60 * 6
INTERVAL_SECONDS = 5

def get_order(time_elapsed):
    orders = []

    # Select the volume of instrument to bid
    bid_volume = random.choice(range(1, BID_VOLUME_HIGH + 1))
    
    # Sample from the above defined parameters appropriate values 
    # For different order parameters 
    bidder = random.choice(ENTITIES)
    bid_time = START_TIME + timedelta(0, time_elapsed)
    bid_instrument = random.choice(INSTRUMENTS)
    l, u = DISTRIBUTION_PARAMETERS[bid_instrument]
    bid_price = random.choice(range(l, u + 1))
    bid_type = random.choice(BID_TYPE)
    status = "ACTIVE"

    # Create a list of orders with the same parameters 
    # but for as many times as the bid volume

    # Order Creation
    for _ in range(bid_volume):
        o = Order(bidder, bid_instrument, bid_price, bid_type,
                    status, bid_time, DEFAULT_TRANSACTION_TIME)
        orders.append(o)
    
    return orders

# Generate all the orders for the given day all at once
def order_generation():
    orders = []
    for intervals in range(N_ORDERS):
        ords = get_order(intervals * INTERVAL_SECONDS)
        orders.extend(ords)
    return orders

# Try out the above code
all_orders = []
for idx, o in enumerate(order_generation()):
    print(f"{idx:0>3d} {o}")
    all_orders.append(o)

pickle.dump(all_orders, open("results/today_order_info.pkl", "wb"))