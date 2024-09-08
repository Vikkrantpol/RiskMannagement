import yfinance as yf
import pandas as pd
import os

# Function to calculate the Exponential Moving Average (EMA)
def calculate_ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()

# Function to get stock data and calculate EMAs (Daily Exponential Moving Averages)
def get_stock_data(symbol):
    stock_data = yf.download(symbol, period="6mo", interval="1d")
    stock_data['5 EMA'] = calculate_ema(stock_data['Close'], 5)
    stock_data['7 EMA'] = calculate_ema(stock_data['Close'], 7)
    stock_data['9 EMA'] = calculate_ema(stock_data['Close'], 9)
    stock_data['12 EMA'] = calculate_ema(stock_data['Close'], 12)
    stock_data['15 EMA'] = calculate_ema(stock_data['Close'], 15)
    stock_data['21 EMA'] = calculate_ema(stock_data['Close'], 21)
    stock_data['50 EMA'] = calculate_ema(stock_data['Close'], 50)
    return stock_data

# Function to calculate the number of stocks to buy and risk
def calculate_position_and_risk(total_capital, cmp, sl):
    max_risk = 0.001 * total_capital  # 0.1% of total capital
    num_stocks = int(max_risk / (cmp - sl))
    actual_risk = (cmp - sl) * num_stocks
    return num_stocks, max_risk, actual_risk

# Function to save the data to a CSV file (append mode)
def save_to_csv(data, filename='stock_analysis.csv'):
    file_exists = os.path.isfile(filename)
    df = pd.DataFrame([data])  # Convert the dictionary to a DataFrame
    df.to_csv(filename, mode='a', header=not file_exists, index=False)  # Append to CSV file

# Main script
def main():
    base_capital = 1500000  # Base capital in rupees

    # Let the user choose the percentage of capital to deploy
    while True:
        deploy_percent = input("Enter the percentage of capital to deploy (3, 5, 7): ")
        if deploy_percent in ['3', '5', '7']:
            deploy_percent = int(deploy_percent)
            break
        else:
            print("Invalid input, please enter 3, 5, or 7.")
    
    capital_to_deploy = (deploy_percent / 100) * base_capital
    print(f"\nThe amount of capital to deploy is: ₹{capital_to_deploy:.2f}")

    # Let the user enter the stock symbol
    stock_symbol = input("Enter the stock symbol (e.g., 'RELIANCE.NS'): ").upper()

    # Fetch stock data and calculate EMAs
    stock_data = get_stock_data(stock_symbol)
    
    # Get the current price (CMP)
    cmp = stock_data['Close'].iloc[-1]
    print(f"\nThe Current Market Price (CMP) of {stock_symbol} is: ₹{cmp:.2f}\n")

    # Check if CMP is below the 50 EMA
    ema_50 = stock_data['50 EMA'].iloc[-1]
    if cmp < ema_50:
        print(f"Don't make any position as CMP ({cmp:.2f}) is below the 50 EMA ({ema_50:.2f})")
        return

    # Print each EMA value on a different line
    print(f"{stock_symbol} EMAs:")
    print(f"5 EMA:  ₹{stock_data['5 EMA'].iloc[-1]:.2f}")
    print(f"7 EMA:  ₹{stock_data['7 EMA'].iloc[-1]:.2f}")
    print(f"9 EMA:  ₹{stock_data['9 EMA'].iloc[-1]:.2f}")
    print(f"12 EMA: ₹{stock_data['12 EMA'].iloc[-1]:.2f}")
    print(f"15 EMA: ₹{stock_data['15 EMA'].iloc[-1]:.2f}")
    print(f"21 EMA: ₹{stock_data['21 EMA'].iloc[-1]:.2f}")
    print(f"50 EMA: ₹{ema_50:.2f}")

    # Let the user choose the stop loss level
    while True:
        stop_loss_ema = input("Choose stop loss EMA (5, 7, 9, 12, 15, 21): ")
        if stop_loss_ema in ['5', '7', '9', '12', '15', '21']:
            stop_loss_ema = int(stop_loss_ema)
            break
        else:
            print("Invalid input, please enter 5, 7, 9, 12, 15, or 21.")

    # Get the selected stop loss (SL)
    sl = stock_data[f'{stop_loss_ema} EMA'].iloc[-1]

    # Check if CMP is below the selected stop loss EMA
    if cmp < sl:
        print(f"SL can't be calculated as CMP ({cmp:.2f}) is below the chosen SL ({sl:.2f}).")
        print("Choose SL that is below CMP.")
        return

    # Calculate the number of stocks to buy, the max risk, and the actual risk
    num_stocks, max_risk, actual_risk = calculate_position_and_risk(base_capital, cmp, sl)

    # Display the results
    print(f"\nThe maximum risk per trade (0.1% of total capital) is: ₹{max_risk:.2f}")
    print(f"With {stop_loss_ema} EMA as Stop Loss ({sl:.2f}), you should buy {num_stocks} shares of {stock_symbol}.")
    print(f"The actual risk for this trade will be: ₹{actual_risk:.2f}")
    print(f"\nThe amount of capital to deploy is: ₹{capital_to_deploy:.2f}")

    # Create data dictionary to save in CSV (excluding EMAs)
    data = {
        'Stock Symbol': stock_symbol,
        'CMP': cmp,
        'Stop Loss EMA': stop_loss_ema,
        'Stop Loss Price': sl,
        'Number of Stocks': num_stocks,
        'Max Risk': max_risk,
        'Actual Risk': actual_risk,
        'Deployed Capital': capital_to_deploy
    }

    # Save the results to a CSV file (append mode)
    save_to_csv(data)
    print(f"\nResults saved to 'stock_analysis.csv'")

if __name__ == "__main__":
    main()
