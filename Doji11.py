import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

def fetch_stock_data(symbol, period='5d'):
    try:
        # Adjusting the number of days to fetch based on the period
        end_date = datetime.now().date()
        if period == '5d':
            start_date = end_date - timedelta(days=7)  # around 1 week
        elif period == '140d':
            start_date = end_date - timedelta(days=200)  # around 200 days to ensure we get at least 140 trading days
        else:
            start_date = end_date - timedelta(days=60)  # default 60 days for other periods
        
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date, interval='1d')

        if data.empty:
            print(f"No data found for {symbol}. Possibly delisted or no trading data available.")
            return None

        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def detect_doji_candles(data):
    try:
        # Calculate percentage difference threshold for doji
        threshold = 0.002  # ±0.2%

        # Initialize counter for doji candles
        doji_count = 0

        # Loop through the last 5 trading days
        for i in range(min(5, len(data))):  # Ensure we do not exceed available data
            open_price = data['Open'].iloc[i]
            close_price = data['Close'].iloc[i]

            # Calculate percentage change
            pct_change = abs(close_price - open_price) / open_price

            # Check if it's a doji candle
            if pct_change <= threshold:
                doji_count += 1
        
        return doji_count

    except Exception as e:
        print(f"Error detecting doji candles: {e}")
        return 0

def plot_candlestick(symbol, data):
    try:
        # Convert DataFrame to the right format for candlestick_ohlc
        data['Date'] = mdates.date2num(data.index.to_pydatetime())
        ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']]

        fig, ax = plt.subplots()
        candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='g', colordown='r')

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.title(f'Candlestick chart for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.tight_layout()

        # Save plot as PNG file in the new directory
        plot_dir = 'doji_candles_plots'
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        plot_file = os.path.join(plot_dir, f'{symbol}_candlestick.png')
        plt.savefig(plot_file)
        plt.close()

        print(f"Saved candlestick plot for {symbol} to {plot_file}")
    except Exception as e:
        print(f"Error plotting candlestick chart for {symbol}: {e}")

def main():
    try:
        # Read stock symbols from the CSV file
        df = pd.read_csv('EQUITY_L.csv')
        symbols = df['SYMBOL'].tolist()

        results = []

        # Current date for the scanning
        scan_date = datetime.now().strftime('%Y-%m-%d')

        # Iterate over each symbol
        for symbol in symbols:
            symbol = symbol.strip().upper() + ".NS"  # Ensure symbol is in uppercase and append '.NS'
            print(f"Processing {symbol}...")

            # Fetch stock data for the last 5 trading days
            data = fetch_stock_data(symbol, period='5d')
            if data is None:
                continue  # Skip to the next symbol if data fetch fails
            
            # Detect doji candles
            doji_count = detect_doji_candles(data)

            # Print and collect result if at least 2 doji candles detected
            if doji_count >= 2:
                print(f"{symbol}: Detected {doji_count} doji candles.")
                results.append({
                    'Symbol': symbol,
                    'DojiCount': doji_count,
                    'ScanDate': scan_date
                })

                # Fetch stock data for the last 140 trading sessions
                data_140d = fetch_stock_data(symbol, period='140d')
                if data_140d is not None:
                    # Generate and save candlestick plot
                    plot_candlestick(symbol, data_140d)

        # Save results to CSV file
        if results:
            results_df = pd.DataFrame(results)
            output_file = 'doji_candles_detection_results.csv'
            if os.path.exists(output_file):
                results_df.to_csv(output_file, mode='a', header=False, index=False)
            else:
                results_df.to_csv(output_file, index=False)
            print(f"\nResults saved to {output_file}.")
        else:
            print("No symbols found with at least 2 doji candles in the last 5 trading sessions.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
