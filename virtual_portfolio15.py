import pandas as pd
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self):
        self.holdings = pd.DataFrame(columns=['Symbol', 'Quantity', 'Buy Price', 'Buy Date'])
        self.cash = 2000000  # Starting with 2,000,000 rupees
        self.transaction_log = []

    def buy_stock(self, symbol, quantity, buy_date):
        current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
        total_value = current_price * quantity
        if self.cash < total_value:
            print("Not enough cash to buy.")
            return False

        self.cash -= total_value
        
        if symbol in self.holdings['Symbol'].values:
            existing_holding = self.holdings[self.holdings['Symbol'] == symbol]
            total_quantity = existing_holding['Quantity'].iloc[0] + quantity
            avg_price = ((existing_holding['Quantity'].iloc[0] * existing_holding['Buy Price'].iloc[0]) + total_value) / total_quantity
            self.holdings.loc[self.holdings['Symbol'] == symbol, 'Quantity'] = total_quantity
            self.holdings.loc[self.holdings['Symbol'] == symbol, 'Buy Price'] = avg_price
        else:
            new_holding = pd.DataFrame({'Symbol': [symbol], 'Quantity': [quantity], 'Buy Price': [current_price], 'Buy Date': [buy_date]})
            self.holdings = pd.concat([self.holdings, new_holding], ignore_index=True)
        
        self.transaction_log.append({'Date': buy_date, 'Action': 'BUY', 'Symbol': symbol, 'Quantity': quantity, 'Price': current_price, 'Total Value': total_value, 'Cash Balance': self.cash})
        return True

    def sell_stock(self, symbol, quantity, sell_date):
        if symbol not in self.holdings['Symbol'].values:
            print(f"No holdings in {symbol}")
            return False

        holding = self.holdings[self.holdings['Symbol'] == symbol]
        if holding['Quantity'].sum() < quantity:
            print(f"Not enough quantity to sell {quantity} shares of {symbol}.")
            return False

        current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
        total_value = current_price * quantity
        self.cash += total_value
        self.transaction_log.append({'Date': sell_date, 'Action': 'SELL', 'Symbol': symbol, 'Quantity': quantity, 'Price': current_price, 'Total Value': total_value, 'Cash Balance': self.cash})

        # Update holdings
        self.holdings.loc[self.holdings['Symbol'] == symbol, 'Quantity'] -= quantity
        self.holdings = self.holdings[self.holdings['Quantity'] > 0]
        return True

    def exit_all(self, sell_date):
        for index, row in self.holdings.iterrows():
            symbol = row['Symbol']
            quantity = row['Quantity']
            current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            total_value = current_price * quantity
            self.cash += total_value
            self.transaction_log.append({'Date': sell_date, 'Action': 'SELL', 'Symbol': symbol, 'Quantity': quantity, 'Price': current_price, 'Total Value': total_value, 'Cash Balance': self.cash})

        self.holdings = pd.DataFrame(columns=['Symbol', 'Quantity', 'Buy Price', 'Buy Date'])

    def get_portfolio_value(self):
        total_value = 0
        for index, row in self.holdings.iterrows():
            symbol = row['Symbol']
            quantity = row['Quantity']
            current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            total_value += quantity * current_price
        total_value += self.cash  # Add cash balance
        return total_value

    def get_pnl(self):
        total_investment = (self.holdings['Quantity'] * self.holdings['Buy Price']).sum()
        current_value = 0
        for index, row in self.holdings.iterrows():
            symbol = row['Symbol']
            current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            current_value += row['Quantity'] * current_price
        return current_value - total_investment

    def print_portfolio(self):
        # Add current price, invested amount, current value, and % change to holdings for display
        holdings_with_values = self.holdings.copy()
        holdings_with_values['Current Price'] = holdings_with_values['Symbol'].apply(lambda symbol: round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2))
        holdings_with_values['Invested Amount'] = round(holdings_with_values['Quantity'] * holdings_with_values['Buy Price'], 2)
        holdings_with_values['Current Value'] = round(holdings_with_values['Quantity'] * holdings_with_values['Current Price'], 2)
        holdings_with_values['% Change'] = round((holdings_with_values['Current Price'] - holdings_with_values['Buy Price']) / holdings_with_values['Buy Price'] * 100, 2)
        
        # Calculate PNL
        pnl = self.get_pnl()

        print(f"Cash: ₹{self.cash:.2f}")
        print("Holdings:")
        print(holdings_with_values.to_string(index=False))
        print(f"Total Portfolio Value: ₹{self.get_portfolio_value():.2f}")
        print(f"Total PNL: ₹{pnl:.2f}")

    def save_portfolio_csv(self, filename="portfolio.csv"):
        # Add current price, invested amount, current value, and % change to holdings for saving
        holdings_with_values = self.holdings.copy()
        holdings_with_values['Current Price'] = holdings_with_values['Symbol'].apply(lambda symbol: round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2))
        holdings_with_values['Invested Amount'] = round(holdings_with_values['Quantity'] * holdings_with_values['Buy Price'], 2)
        holdings_with_values['Current Value'] = round(holdings_with_values['Quantity'] * holdings_with_values['Current Price'], 2)
        holdings_with_values['% Change'] = round((holdings_with_values['Current Price'] - holdings_with_values['Buy Price']) / holdings_with_values['Buy Price'] * 100, 2)
        holdings_with_values.to_csv(filename, index=False)

    def load_portfolio_csv(self, filename="portfolio.csv"):
        self.holdings = pd.read_csv(filename)

    def save_transaction_log(self, filename="transaction_log.txt"):
        with open(filename, 'a') as f:
            for transaction in self.transaction_log:
                f.write(f"{transaction}\n")
    def generate_bar_graph(self):
    # Prepare data for bar graph
          symbols = self.holdings['Symbol']
          current_prices = [round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2) for symbol in symbols]
          buy_prices = self.holdings['Buy Price']
          quantities = self.holdings['Quantity']

    # Calculate total investment and current value for each holding
          total_investment = buy_prices * quantities
          current_value = current_prices * quantities

    # Create a bar graph
          fig, ax = plt.subplots(figsize=(10, 6))
          width = 0.35
          ind = range(len(symbols))
          bars1 = ax.bar(ind, total_investment, width, label='Total Investment')
          bars2 = ax.bar([x + width for x in ind], current_value, width, label='Current Value')

          ax.set_ylabel('Value')
          ax.set_title('Total Investment vs Current Value')
          ax.set_xticks([x + width / 2 for x in ind])
          ax.set_xticklabels(symbols)
          ax.legend()

          plt.xticks(rotation=45, ha='right')
          plt.tight_layout()

    # Save the bar graph as an image
          plt.savefig('portfolio_value_bar_graph.png')
          plt.show()


##    def generate_bar_graph(self):
##        # Prepare data for bar graph
##        symbols = self.holdings['Symbol']
##        current_prices = [round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2) for symbol in symbols]
##        buy_prices = self.holdings['Buy Price']
##        quantities = self.holdings['Quantity']
##
##        # Calculate total investment and current value for each holding
##        total_investment = buy_prices * quantities
##        current_value = current_prices * quantities
##
##        # Create a bar graph
##        fig, ax = plt.subplots(figsize=(10, 6))
##        width = 0.35
##        ind = range(len(symbols))
##        bars1 = ax.bar(ind, total_investment, width, label='Total Investment')
##        bars2 = ax.bar(ind, current_value, width, bottom=total_investment, label='Current Value')
##
##        ax.set_ylabel('Value')
##        ax.set_title('Total Investment vs Current Value')
##        ax.set_xticks(ind)
##        ax.set_xticklabels(symbols)
##        ax.legend()
##
##        plt.xticks(rotation=45, ha='right')
##        plt.tight_layout()
##
##        # Save the bar graph as an image
##        plt.savefig('portfolio_value_bar_graph.png')
##        plt.show()

def main():
    portfolio = Portfolio()
    portfolio.load_portfolio_csv()  # Load portfolio data from CSV

    while True:
        action = input("Enter 'buy' to buy a stock, 'sell' to sell a stock, 'exit all' to sell all holdings, 'exit' to exit: ").strip().lower()
        if action == 'exit':
            break

        if action == 'buy':
            symbol = input("Enter stock symbol: ").strip().upper()
            current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            print(f"Current market price (CMP) of {symbol} is ₹{current_price:.2f}")
            quantity = int(input("Enter quantity: "))
            buy_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            success = portfolio.buy_stock(symbol, quantity, buy_date)
            if success:
                print(f"Bought {quantity} shares of {symbol} at ₹{current_price:.2f} each. Total value: ₹{quantity * current_price:.2f}")
            else:
                print("Failed to buy stock.")
        elif action == 'sell':
            print("Current Holdings:")
            portfolio.print_portfolio()
            symbol = input("Enter stock symbol from your holdings: ").strip().upper()
            quantity = int(input("Enter quantity: "))
            current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            sell_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            success = portfolio.sell_stock(symbol, quantity, sell_date)
            if success:
                print(f"Sold {quantity} shares of {symbol} at ₹{current_price:.2f} each. Total value: ₹{quantity * current_price:.2f}")
            else:
                print("Failed to sell stock.")
        elif action == 'exit all':
            sell_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            portfolio.exit_all(sell_date)
            print("All holdings sold.")
        else:
            print("Invalid action. Please enter 'buy', 'sell', 'exit all', or 'exit'.")

        print(f"Available funds: ₹{portfolio.cash:.2f}")

    portfolio.print_portfolio()
    portfolio.save_portfolio_csv()  # Save portfolio data to CSV
    portfolio.save_transaction_log()
    print("Portfolio and transaction log saved.")

    # Generate bar graph
    portfolio.generate_bar_graph()

if __name__ == "__main__":
    main()

