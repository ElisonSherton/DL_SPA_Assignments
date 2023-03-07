# Subscribe to both topics order buy and order sell
# Run the logic to create match and execute transactions
from utils import *
random.seed(42)

from collections import Counter
from tqdm import tqdm

# Define paths to the order info database and where to store the trades happening for the given orders
ORDER_INFO = "results/today_order_info.pkl"
TRADE_DB_PATH = "results/today_day_trades.pkl"

# Read the order information
order_data = pickle.load(open(ORDER_INFO, "rb"))

# Get the instruments traded in the exchange
instruments = json.load(open(INSTRUMENTS_DATA, "r"))

# Get all the bidders information who have placed orders
entities = set([x.bidder for x in order_data])

# Logic to perform order matching
# FIFO Logic 
def resolve_instrument(orders, instrument):
    trades = []
    
    # Segregate the buy and sell orders for the instrument of our choice
    i_buy = [x for x in orders if ((x.bid_instrument == instrument) and (x.bid_type == "Buy"))]
    i_sell = [x for x in orders if ((x.bid_instrument == instrument) and (x.bid_type == "Sell"))]
    
    # Loop over all the sell orders
    for sell_order in tqdm(i_sell, total = len(i_sell), desc = f"Matchmaking for {instrument}"):
        
        # Only if the sell order is active, proceed ahead else, loop over the next sell order
        if sell_order.bid_status != "ACTIVE":
            continue
        
        # Get a subset of the buys for the instrument older than the current timestamp
        # And sort all of these in the chronological order
        older_buys = [x for x in i_buy if sell_order.bid_time >= x.bid_time]
        older_buys = sorted(older_buys, key = lambda x: x.bid_time)
        
        # Try finding a buy order in chronological order
        for buy_order in older_buys:
            
            # If the current buy order is not active, skip and loop over to the next order
            if buy_order.bid_status != "ACTIVE":
                continue
            
            # If we find a match, then deactivate this buy and the corresponding sell order
            # And populate their transaction times as the larger of the two bid times
            if buy_order.bid_price == sell_order.bid_price:
                transact_time = max(buy_order.bid_time, sell_order.bid_time)
                
                buy_order.bid_status = "BOUGHT"
                sell_order.bid_status = "SOLD"
                
                buy_order.transaction_time = transact_time
                sell_order.transaction_time = transact_time
                
                # Accumulate the trade information in an array buy storing the buy and sell order
                trades.append([buy_order, sell_order])
                
    # Return the orders and the trades performed
    return orders, trades

trades = []
for instrument in instruments:
    order_data, instrument_trades = resolve_instrument(order_data, instrument)
    trades.extend(instrument_trades)

# Store the trades that took place in a database (here a pickle file)
pickle.dump(trades, open(TRADE_DB_PATH, "wb"))