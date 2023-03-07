# Subscribe to both topics order buy and order sell
# Run the logic to create match and execute transactions
from utils import *
random.seed(42)

from collections import Counter
from tqdm import tqdm
import logging, time

# Set the level to INFO
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths to the order info database and where to store the trades happening for the given orders
ORDER_INFO = "../results_dynamic/today_order_info.pkl"
TRADE_DB_PATH = "../results_dynamic/today_day_trades.pkl"

# Get the instruments traded in the exchange
INSTRUMENTS_DATA = "../data/marketplace_instruments.json"
instruments = json.load(open(INSTRUMENTS_DATA, "r"))

# Define the time at which the exchange shuts down
EXCHANGE_SHUT_TIME = datetime(2023, 2, 28, 15, 30, 0)

# Define the time for which to sleep between execution of the matching engine
TRADE_MATCH_TIME = 2 # 2 seconds

# Logic to perform order matching
# FIFO Logic 
def resolve_instrument(orders, instrument):
    trades = []
    
    # Segregate the buy and sell orders for the instrument of our choice
    i_buy = [x for x in orders if ((x.bid_instrument == instrument) and (x.bid_type == "Buy"))]
    i_sell = [x for x in orders if ((x.bid_instrument == instrument) and (x.bid_type == "Sell"))]
    
    # Loop over all the sell orders
    for sell_order in i_sell:#, total = len(i_sell), desc = f"Matchmaking for {instrument}"):
        
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


if __name__ == "__main__":
    trades = []
    
    while True:
        # Read the order information
        order_data = pickle.load(open(ORDER_INFO, "rb"))

        for instrument in instruments:
            order_data, instrument_trades = resolve_instrument(order_data, instrument)
            trades.extend(instrument_trades)

        # Store the trades that took place in a database (here a pickle file)
        pickle.dump(trades, open(TRADE_DB_PATH, "wb"))
        
        # Store the order information back in the orders database (since we've possibly modified transaction time of some orders)
        pickle.dump(order_data, open(ORDER_INFO, "wb"))
        
        # Breaking Condition
        # We know trades for the day end at 15:30 hours, so we can stop when the latest order placed is matched against the existing repositories of trading
        last_order = order_data[-1]
        if (last_order.bid_time.hour == 15) and (last_order.bid_time.minute == 30):
            break
        
        # If trade happened, print it to the console
        for t in instrument_trades:
            logging.info(f"Trades happening in this time interval as follows")
            b, s = t
            logging.info(str(b))
            logging.info(str(s))
            
        # Sleep for some time
        time.sleep(TRADE_MATCH_TIME)