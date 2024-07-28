import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Step 1: Read the CSV file and extract the stock symbols
try:
    df = pd.read_csv('EQUITY_L.csv')
    symbols = df['SYMBOL'].tolist()
    print(f"Successfully read {len(symbols)} symbols from EQUITY_L.csv.")
except Exception as e:
    print(f"Error reading EQUITY_L.csv: {e}")
    symbols = []

# Step 2: Define the timeframe for the 52-week period
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Step 3: Function to check for fresh 52-week breakout
def is_fresh_52_week_breakout(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")  # Assuming Indian stocks with .NS suffix
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            print(f"No historical data for {symbol}")
            return False
        
        # Calculate the 52-week high
        hist['52_week_high'] = hist['High'].rolling(window=252, min_periods=1).max()
        
        latest_high = hist['High'].iloc[-1]
        previous_52_week_high = hist['52_week_high'].iloc[-2]
        
        if latest_high > previous_52_week_high:
            print(f"{symbol} is a fresh 52-week breakout.")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return False

# Step 4: Check each symbol for a fresh 52-week breakout
breakout_stocks = []
for symbol in symbols:
    if is_fresh_52_week_breakout(symbol):
        breakout_stocks.append(symbol)

# Step 5: Save the output to a new CSV file
if breakout_stocks:
    breakout_df = pd.DataFrame(breakout_stocks, columns=['SYMBOL'])
    breakout_df.to_csv('52_week_breakouts.csv', index=False)
    print("Breakout stocks saved in 52_week_breakouts.csv")
else:
    print("No breakout stocks found.")
