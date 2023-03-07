# Compute simple moving average over all the trades happening over the course of one day 
from utils import *
random.seed(42)
from PIL import Image
from pathlib import Path

from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt
plt.style.use("ggplot")

# Define the path to trades in the database and specify the path where to store the SMA
TRADE_DB_PATH = "results/today_day_trades.pkl"
SMA_PATH = "results/today_sma_information.pkl"

# Read the order information
trade_data = pickle.load(open(TRADE_DB_PATH, "rb"))

# Obtain all the instruments and bidders who have placed orders
instruments = json.load(open(INSTRUMENTS_DATA, "r"))

# Define the start and end times i.e. bounds within which to compute the SMA
START_TIME = datetime(2023, 2, 28, 9, 30)
END_TIME = datetime(2023, 2, 28, 15, 30)

# Define the SMA and the window duration respectively
SMA_DURATION = 10 * 60 # 10 minutes
WINDOW_DURATION = 5 * 60 # 5 minutes
GIF_SCREEN_DURATION = 500 # Frame rate of 2 frames per second (500 milliseconds per image)

# Define the bounds that we have computed to better plot the SMA
plot_bounds = {"Rakuten": [388, 422], "Karza": [8, 22], "Infosys": [1498, 1522]}

# Logic to compute SMA at a time interval of 5 minutes with a sliding window of 10 minutes 
def sma_computation(instrument, trades, window_duration = 5 * 60, sma_duration = 10 * 60):
    
    # Start right from the beginning
    current_time = START_TIME
    
    # Store the values of the trades which are happening in a dictionary
    sma_map = {}
    
    # Loop over all the time tickers and check the trades for the instrument of choice
    # Compute the SMA in steps of window duration by considering a window of sma_duration
    while current_time < END_TIME:
        current_time = current_time + timedelta(0, window_duration)
        start = current_time - timedelta(0, sma_duration)

        window_start = max(START_TIME, start)
        window_end = min(END_TIME, current_time)

        bid_sum = 0; bid_count = 0;
        for trade in trades:
            if ((trade[0].transaction_time >= window_start) and (trade[0].transaction_time < window_end)):
                if trade[0].bid_instrument == instrument:
                    bid_sum += trade[0].bid_price
                    bid_count += 1

        sma_map[window_end] = [bid_sum, bid_count, round(bid_sum / bid_count, 3)]        
    return sma_map

def plot_sma_computation(sma_map, instrument):
    
    timestamps = list(sma_map.keys())
    moving_averages = [x[-1] for x in sma_map.values()]
    
    # Create images of moving averages
    limits = plot_bounds[instrument]
    
    # Create the plots and the gif
    for idx in tqdm(range(len(timestamps)), desc = f"Plotting SMA for {instrument} chronologically"):
        # Find out the x, y, label, mean etc.
        sub_timestamps = timestamps[:(idx + 1)]
        sub_moving_averages = moving_averages[:(idx + 1)]
        title = sub_timestamps[-1].strftime(f"SMA for {instrument} as of %H-%M")
        absolute_mean = sum(sub_moving_averages) / len(sub_moving_averages)
        
        # Create the figure now
        plt.figure(figsize = (20,5))
        plt.plot([x.strftime("%H-%M") for x in sub_timestamps], sub_moving_averages)
        plt.xticks(rotation = 90);
        plt.title(title, fontsize = 20);
        plt.hlines(absolute_mean, 0, idx + 1, linestyles = "dotted", color = "b");
        plt.ylim(limits)
        plt.ylabel("Trade Price in INR")
        plt.xlabel("Timestamp")
        plt.text(0, absolute_mean + 0.5, f"Absolute Mean: {absolute_mean:.2f}", fontsize = 10)
        plt.savefig(f"images/image_{idx}.png")
        plt.close()

    # Create a gif out of the images created above
    image_paths = [x for x in Path("images").glob("*") if x.suffix == ".png"]
    image_paths = sorted(image_paths, key = lambda x: int(x.stem.split("_")[-1]), reverse = False)
    images = []
    for i in image_paths:
        images.append(Image.open(i))

    images[0].save(f'images/SMA_{instrument}.gif',
                   save_all = True,
                   append_images = images[1:],
                   duration = GIF_SCREEN_DURATION,
                   loop = 0)

    # Delete all the png images
    for i in image_paths: i.unlink()

# Loop over all the instruments and plot their respective SMAs
sma_info = {}
for instrument in instruments:
    # Compute the simple moving average
    sma_map =  sma_computation(instrument, trade_data)
    
    # Plot the same against time
    plot_sma_computation(sma_map, instrument)
    
    # Keep the information in a map
    sma_info[instrument] = sma_map
    
# Store the trades that took place in a database (here a pickle file)
pickle.dump(sma_info, open(SMA_PATH, "wb"))