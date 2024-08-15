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

def get_stop_loss(stock_symbol, use_day_low=False, ema_days=None):
    try:
        stock = yf.Ticker(stock_symbol)
        if use_day_low:
            data = stock.history(period="1d")
            if not data.empty:
                day_low = data['Low'].iloc[-1]
                return day_low
            else:
                print(f"No data found for {stock_symbol}.")
                return None
        elif ema_days:
            history_data = stock.history(period="6mo")
            if len(history_data) >= max(ema_days):
                ema_values = {}
                for days in ema_days:
                    ema = history_data['Close'].ewm(span=days, adjust=False).mean().iloc[-1]
                    ema_values[days] = ema
                return ema_values
            else:
                print("Not enough data to calculate EMAs.")
                return None
        else:
            data = stock.history(period="1d")
            if not data.empty:
                stop_loss = data['Open'].iloc[-1]
                return stop_loss
            else:
                print(f"No data found for {stock_symbol}.")
                return None
    except Exception as e:
        print(f"Error fetching stop loss data: {e}")
        return None

def get_last_session_close(stock_symbol):
    """Fetches the last session's closing price for a given stock symbol."""
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d")
        if not data.empty:
            last_session_close = data['Close'].iloc[-1]
            return last_session_close
        else:
            print(f"No data found for {stock_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching last session's closing price: {e}")
        return None

def main():
    stock_symbol = input("Enter stock symbol (e.g., RELIANCE.NS): ")
    capital = 1445000
    
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
            position_size, capital_deployed, max_risk, percentage_risk_per_entire_capital, no_of_shares = position_data
            
            print(f"Position Size: {position_size}%")
            print(f"Capital Deployed: Rs.{capital_deployed:.2f}")
            print(f"Max Risk: Rs.{max_risk:.2f}")
            print(f"% Risk per Entire Capital: {percentage_risk_per_entire_capital:.2f}%")
            print(f"No of Shares: {no_of_shares}")
            
            # Ask the user to select the stop loss option
            print("\nSelect the stop loss option:")
            print("1. Day's Low Price")
            print("2. Last Session's Closing Price")
            print("3. Custom Stop Loss (Percentage of CMP)")
            print("4. EMA Stop Loss (Options: 5d, 7d, 9d, 12d, 15d, 18d, 21d, 50d)")
            
            option = input("Enter option number (1/2/3/4): ").strip()

            if option == "1":
                custom_stop_loss = get_stop_loss(stock_symbol, use_day_low=True)
            elif option == "2":
                custom_stop_loss = get_last_session_close(stock_symbol)
            elif option == "3":
                try:
                    custom_stop_loss_percent = float(input("Enter custom stop loss percentage (e.g., 2.5 for 2.5%): "))
                    custom_stop_loss = cmp - (cmp * (custom_stop_loss_percent / 100))
                except ValueError:
                    print("Invalid input. Using default stop loss.")
                    custom_stop_loss = get_stop_loss(stock_symbol)
            elif option == "4":
                ema_days = [5, 7, 9, 12, 15, 18, 21, 50]
                ema_stop_losses = get_stop_loss(stock_symbol, ema_days=ema_days)
                if ema_stop_losses:
                    print("Available EMAs and their values:")
                    for days, ema in ema_stop_losses.items():
                        print(f"{days}-day EMA: {ema}")
                    
                    selected_days = input("Enter the EMA days you want to use (choose from 5, 7, 9, 12, 15, 18, 21, 50): ").strip()
                    try:
                        selected_days = int(selected_days)
                        if selected_days in ema_days:
                            custom_stop_loss = ema_stop_losses[selected_days]
                        else:
                            print("Invalid EMA days selected. Using default stop loss.")
                            custom_stop_loss = get_stop_loss(stock_symbol)
                    except ValueError:
                        print("Invalid input. Using default stop loss.")
                        custom_stop_loss = get_stop_loss(stock_symbol)
                else:
                    print("Unable to fetch EMA data. Using default stop loss.")
                    custom_stop_loss = get_stop_loss(stock_symbol)
            else:
                print("Invalid option selected. Using default stop loss.")
                custom_stop_loss = get_stop_loss(stock_symbol)

            # Calculate percentage risk on deployed capital and entire capital
            if custom_stop_loss:
                max_risk = (cmp - custom_stop_loss) * no_of_shares
                percentage_risk_on_deployed = (max_risk / capital_deployed) * 100
                percentage_risk_on_entire = (max_risk / capital) * 100
            else:
                print("Unable to calculate stop loss.")
                return

            output = (f"Date Time: {current_datetime}\n"
                      f"Stock: {stock_symbol}\n"
                      f"Price: {price}\n"
                      f"Change: {change}\n"
                      f"Position Size: {position_size}%\n"
                      f"Capital Deployed: Rs.{capital_deployed:.2f}\n"
                      f"Max Risk: Rs.{max_risk:.2f}\n"
                      f"% Risk on Deployed Capital: {percentage_risk_on_deployed:.2f}%\n"
                      f"% Risk per Entire Capital: {percentage_risk_on_entire:.2f}%\n"
                      f"No of Shares: {no_of_shares}\n"
                      f"Stop Loss: {custom_stop_loss:.2f}")

            if percentage_risk_on_entire > 0.5:
                print("Be careful, You are risking more than 0.5% of your capital.")

            # Print the output
            print(output)
            save_to_csv([current_datetime, stock_symbol, price, change, position_size, 
                      capital_deployed, max_risk, percentage_risk_on_entire, no_of_shares, custom_stop_loss])
            save_to_text(output)
    else:
        print("Stock data not found or unable to fetch data. Consider using official APIs.")
        print("Here are some alternative options for reliable stock data:")
        print("- NSE Data API: https://www.nseindia.com/market-data/real-time-data-subscription")
        print("- Alpha Vantage: https://www.alphavantage.co/documentation/")

if __name__ == "__main__":
    main()
