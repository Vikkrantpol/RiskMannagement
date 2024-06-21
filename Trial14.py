import yfinance as yf
import datetime
import csv
import os

def get_last_trading_day():
    """Returns the last trading day (i.e., a weekday that is not a holiday)."""
    today = datetime.datetime.now()
    # Define known trading holidays for 2024 in YYYY-MM-DD format.
    trading_holidays = [
        "2024-01-26", "2024-03-29", "2024-04-08", "2024-04-14", "2024-05-01",
        "2024-08-15", "2024-08-19", "2024-10-02", "2024-10-31", "2024-11-15",
        "2024-12-25"
    ]
    
    # Check if today is a weekend or a trading holiday.
    while today.weekday() > 4 or today.strftime("%Y-%m-%d") in trading_holidays:
        today -= datetime.timedelta(days=1)  # Go back one day.
    
    return today.strftime("%Y-%m-%d")

def get_stock_data(stock_symbol):
    """Fetches the price and percentage change for a given stock symbol from Yahoo Finance.

    Args:
        stock_symbol (str): The stock symbol to search for (e.g., "RELIANCE.NS").

    Returns:
        tuple: A tuple containing the price (str), percentage change (str), or None if the data is not found.
    """
    try:
        stock = yf.Ticker(stock_symbol)
        last_trading_day = get_last_trading_day()
        data = stock.history(period="5d")  # Get data for the last five days
        
        if len(data) >= 2:
            latest_close = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2]
            change = latest_close - previous_close
            change_percent = (change / previous_close) * 100
            return f"{latest_close:.2f}", f"{change_percent:.2f}%"
        else:
            print(f"No sufficient data found for {stock_symbol}.")
            return None, None

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

def save_to_csv(data):
    """Saves the data to a CSV file along with the current date and time.

    Args:
        data (list): The data to be saved to the file.
    """
    try:
        filename = "stock_data_and_position_size_log.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date Time", "Stock Symbol", "Price", "Change (%)",
                                 "Position Size (%)", "Capital Deployed", "Max Risk", 
                                 "% Risk per Entire Capital", "No of Shares", "Stop Loss"])
            writer.writerow(data)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def save_to_text(data):
    """Saves the data to a text file along with the current date and time.

    Args:
        data (str): The data to be saved to the file.
    """
    try:
        filename = "stock_data_and_position_size_log.txt"
        with open(filename, "a") as file:
            file.write(data)
            file.write("\n\n")
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def calculate_position_size(capital, cmp, change_percent):
    if 0.01 <= change_percent <= 0.5:
        position_size = 0.25
    elif 0.5 < change_percent <= 1:
        position_size = 0.225
    elif 1 < change_percent <= 1.5:
        position_size = 0.165
    elif 1.5 < change_percent <= 2:
        position_size = 0.125
    elif 2 < change_percent <= 2.5:
        position_size = 0.10
    elif 2.5 < change_percent <= 3:
        position_size = 0.08
    elif 3 < change_percent <= 3.5:
        position_size = 0.06
    else:
        return None, "Don't make any New Positions."

    capital_deployed = capital * position_size
    max_risk = change_percent * capital_deployed / 100
    percentage_risk_per_entire_capital = (max_risk / capital) * 100
    no_of_shares = int(capital_deployed / cmp)

    return (position_size * 100, capital_deployed, max_risk, percentage_risk_per_entire_capital, no_of_shares), None

def get_stop_loss(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d")
        if not data.empty:
            stop_loss = data['Open'].iloc[-1]  # Using iloc to access by position
            return stop_loss
        else:
            return None
    except Exception as e:
        print(f"Error fetching stop loss data: {e}")
        return None

def main():
    stock_symbol = input("Enter stock symbol (e.g., RELIANCE.NS): ")
    capital = 1208000
    
    price, change = get_stock_data(stock_symbol)

    if price and change:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmp = float(price)
        change_percent = float(change.strip("%"))

        print(f"Current Market Price (CMP): {cmp}")
        print(f"Percentage Change: {change}%")
        
        position_data, error = calculate_position_size(capital, cmp, change_percent)
        
        if error:
            print(error)
        else:
            position_size, capital_deployed, max_risk, percentage_risk, no_of_shares = position_data
            print(f"Capital Deployed: Rs.{capital_deployed}")
            
            # Ask the user if they want to choose a custom stop loss
            use_custom_stop_loss = input("Do you want to choose a custom stop loss? (yes/no): ").strip().lower()
            if use_custom_stop_loss == "yes":
                try:
                    custom_stop_loss = float(input("Enter your custom stop loss price: "))
                    max_risk = (cmp - custom_stop_loss) * no_of_shares
                    percentage_risk = (max_risk / capital) * 100
                except ValueError:
                    print("Invalid stop loss price entered. Using the default stop loss.")
                    custom_stop_loss = get_stop_loss(stock_symbol)
            else:
                custom_stop_loss = get_stop_loss(stock_symbol)
                
            output = (f"Date Time: {current_datetime}\n"
                      f"Stock: {stock_symbol}\n"
                      f"Price: {price}\n"
                      f"Change: {change}\n"
                      f"Position Size: {position_size}%\n"
                      f"Capital Deployed: Rs.{capital_deployed}\n"
                      f"Max Risk: Rs.{max_risk}\n"
                      f"% Risk per Entire Capital: {percentage_risk}%\n"
                      f"No of Shares: {no_of_shares}\n"
                      f"Stop Loss: {custom_stop_loss}")
            
            # Print the output
            print(output)
            save_to_csv([current_datetime, stock_symbol, price, change, position_size, 
                      capital_deployed, max_risk, percentage_risk, no_of_shares, custom_stop_loss])
            save_to_text(output)
    else:
        print("Stock data not found or unable to fetch data. Consider using official APIs.")
        print("Here are some alternative options for reliable stock data:")
        print("- NSE Data API: https://www.nseindia.com/market-data/real-time-data-subscription")
        print("- Alpha Vantage: https://www.alphavantage.co/documentation/")

if __name__ == "__main__":
    main()

