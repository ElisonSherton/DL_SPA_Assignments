import pickle, json
from datetime import datetime
from utils import *

# Path to databases of trades
OLD_TRADES = "../results/previous_day_trades.pkl"
CURRENT_DAY_TRADES = "../results/today_day_trades.pkl"
INSTRUMENTS_DATA = "../data/marketplace_instruments.json"

def close_price_computation(trades, instrument):
    # Set the start and end times for computation of the profit value
    dt = trades[0][0].bid_time
    CLOSE_COMPUTATION_START_TIME = datetime(dt.year, dt.month, dt.day, 15, 0)
    CLOSE_COMPUTATION_END_TIME = datetime(dt.year, dt.month, dt.day, 15, 30)
    
    # Filter out trades pertinent to our instrument and within the specified time period
    traded_amount = 0; traded_volume = 0
    for trade in trades:
        b, s = trade
        # Check for the time constraint
        if (b.transaction_time >= CLOSE_COMPUTATION_START_TIME) and (b.transaction_time < CLOSE_COMPUTATION_END_TIME):
            # Check for the instrument
            if b.bid_instrument == instrument:
                traded_amount += b.bid_price
                traded_volume += 1
        
    # Compute the closing price i.e. average of the prices at which trade has happened so far
    closing_price = traded_amount / traded_volume
    
    return closing_price

# Read yesterday's and today's trades
old_trades = pickle.load(open(OLD_TRADES, "rb"))
current_trades = pickle.load(open(CURRENT_DAY_TRADES, "rb"))

# Get the instruments traded in the exchange
instruments = json.load(open(INSTRUMENTS_DATA, "r"))

# Compute the profit per day for all the instruments
# Assume the previous day's close price as the current day's open price for the sake
# of simplicity and the close price for today as the current day's close price.
# Profit per instrument = Closing price of Current Day - Closing price of Previous Day
profit_map = {}
for instrument in instruments:
    opening_price = close_price_computation(old_trades, instrument)
    closing_price = close_price_computation(current_trades, instrument)
    instrument_profit = closing_price - opening_price
    profit_map[instrument] = instrument_profit

# Sort based on decreasing order of profits
sorted_profit_making_instruments = sorted(profit_map, key = lambda x: profit_map[x], reverse = True)

for k in sorted_profit_making_instruments:
    val = profit_map[k]
    if val > 0:
        print(f"Instrument: {k:<8} | Gain: {val:.2f}")
    else:
        print(f"Instrument: {k:<8} | Loss: {val:.2f}")

# Print the lowest loss making/ highest profit making instrument
highest_profit_instrument = sorted_profit_making_instruments[0]
mag = profit_map[highest_profit_instrument]
if mag > 0:
    print(f"Instrument {highest_profit_instrument} has made the highest profit of {mag:.2f}")
else:
    print(f"Instrument {highest_profit_instrument} has incurred the lowest losses of {mag: .2f}")