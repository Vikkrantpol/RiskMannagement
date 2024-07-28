import pandas as pd
import yfinance as yf

# Function to calculate moving averages and identify Golden Crossovers
def golden_cross(stock_data, short_window=50, long_window=200):
    stock_data['Short_MA'] = stock_data['Close'].rolling(window=short_window, min_periods=1).mean()
    stock_data['Long_MA'] = stock_data['Close'].rolling(window=long_window, min_periods=1).mean()
    
    # Identify Golden Crossovers
    stock_data['Golden_Crossover'] = (stock_data['Short_MA'] > stock_data['Long_MA']) & (stock_data['Short_MA'].shift(1) <= stock_data['Long_MA'].shift(1))
    
    return stock_data

# Read stock symbols from the CSV file
stocks_df = pd.read_csv('EQUITY_L.csv')
symbols = stocks_df['SYMBOL'].tolist()

# Store results in a list
results = []

# Iterate through each symbol and perform Golden Crossover calculation
for symbol in symbols:
    print(f"Processing {symbol}...")
    try:
        stock_data = yf.download(symbol + ".NS", period="1y", interval="1d")  # ".NS" is used for NSE symbols on Yahoo Finance
        if stock_data.empty:
            print(f"No data found for {symbol}")
            continue
        stock_data.reset_index(inplace=True)  # Ensure 'Date' is a column
        
        stock_data = golden_cross(stock_data)
        
        # Convert the 'Date' column to datetime.date for comparison
        stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.date
        
        # Filter rows where Golden Crossover is identified within the last 7 sessions
        recent_golden_crosses = stock_data[stock_data['Golden_Crossover']].copy()
        if not recent_golden_crosses.empty:
            cutoff_date = (pd.Timestamp.now() - pd.DateOffset(days=10)).date()
            recent_golden_crosses = recent_golden_crosses[recent_golden_crosses['Date'] >= cutoff_date]
            if not recent_golden_crosses.empty:
                recent_golden_crosses.loc[:, 'Symbol'] = symbol
                results.append(recent_golden_crosses[['Symbol', 'Date', 'Close', 'Short_MA', 'Long_MA', 'Golden_Crossover']])
        
    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Concatenate all results
if results:
    final_df = pd.concat(results)

    # Save to a new CSV file
    final_df.to_csv('golden_cross_results.csv', index=False)
    print("Golden Crossover scan completed and results saved to golden_cross_results.csv")
else:
    print("No Golden Crossovers found.")
