import yfinance as yf
import mplfinance as mpf
import csv
import os
import matplotlib.pyplot as plt

def format_to_thousand_crores(value):
    return value / 1e7

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Get historical market data for the past year
    hist = stock.history(period="1y")
    
    # Calculate highest/lowest price and volume over the last 365 days
    highest_price = hist['Close'].max()
    lowest_price = hist['Close'].min()
    highest_volume = hist['Volume'].max()
    lowest_volume = hist['Volume'].min()
    
    # Get Market Cap
    market_cap = stock.info.get('marketCap', 'N/A')
    
    # Get Revenue and Profit for the last 4 quarters
    financials = stock.financials
    revenues = financials.loc['Total Revenue']
    profits = financials.loc['Net Income']
    
    # Only keep the last 4 quarters
    last_4_quarters_revenue = revenues[:4]
    last_4_quarters_profit = profits[:4]
    
    # Additional info (like sector, industry, and P/E ratio)
    sector = stock.info.get('sector', 'N/A')
    industry = stock.info.get('industry', 'N/A')
    pe_ratio = stock.info.get('trailingPE', 'N/A')

    # Display the information
    print(f"\nStock Ticker: {ticker}")
    print(f"365-Day High Price: ₹{highest_price:.2f}")
    print(f"365-Day Low Price: ₹{lowest_price:.2f}")
    print(f"365-Day High Volume: {highest_volume}")
    print(f"365-Day Low Volume: {lowest_volume}")
    print(f"Market Cap: ₹{format_to_thousand_crores(market_cap):,.2f} thousand crores")
    
    print("\nLast 4 Quarters Revenue (in thousand crores):")
    for date, revenue in last_4_quarters_revenue.items():
        print(f"{date}: ₹{format_to_thousand_crores(revenue):,.2f} thousand crores")
    
    print("\nLast 4 Quarters Profit (in thousand crores):")
    for date, profit in last_4_quarters_profit.items():
        print(f"{date}: ₹{format_to_thousand_crores(profit):,.2f} thousand crores")
    
    print(f"\nSector: {sector}")
    print(f"Industry: {industry}")
    print(f"P/E Ratio: {pe_ratio}")
    
    stock_data = {
        "Stock Ticker": ticker,
        "365-Day High Price": highest_price,
        "365-Day Low Price": lowest_price,
        "365-Day High Volume": highest_volume,
        "365-Day Low Volume": lowest_volume,
        "Market Cap": format_to_thousand_crores(market_cap),
        "Sector": sector,
        "Industry": industry,
        "P/E Ratio": pe_ratio,
        "Last 4 Quarters Revenue": {date: format_to_thousand_crores(revenue) for date, revenue in last_4_quarters_revenue.items()},
        "Last 4 Quarters Profit": {date: format_to_thousand_crores(profit) for date, profit in last_4_quarters_profit.items()}
    }

    return stock_data, last_4_quarters_revenue, last_4_quarters_profit

def save_to_files(all_stock_data):
    # Save data to a single CSV file
    csv_file = "all_stocks_info.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Stock Ticker", "365-Day High Price", "365-Day Low Price", "365-Day High Volume",
                             "365-Day Low Volume", "Market Cap (in thousand crores)", "Sector", "Industry", "P/E Ratio"])
        for stock_data in all_stock_data:
            writer.writerow([stock_data["Stock Ticker"], stock_data["365-Day High Price"], stock_data["365-Day Low Price"],
                             stock_data["365-Day High Volume"], stock_data["365-Day Low Volume"], 
                             stock_data["Market Cap"], stock_data["Sector"], stock_data["Industry"], stock_data["P/E Ratio"]])
            writer.writerow(["Last 4 Quarters Revenue (in thousand crores)"])
            for date, revenue in stock_data["Last 4 Quarters Revenue"].items():
                writer.writerow([date, revenue])
            writer.writerow([])
            writer.writerow(["Last 4 Quarters Profit (in thousand crores)"])
            for date, profit in stock_data["Last 4 Quarters Profit"].items():
                writer.writerow([date, profit])
            writer.writerow([])

    # Save data to a single text file
    text_file = "all_stocks_info.txt"
    with open(text_file, mode='a') as file:
        for stock_data in all_stock_data:
            file.write(f"Stock Ticker: {stock_data['Stock Ticker']}\n")
            file.write(f"365-Day High Price: ₹{stock_data['365-Day High Price']:.2f}\n")
            file.write(f"365-Day Low Price: ₹{stock_data['365-Day Low Price']:.2f}\n")
            file.write(f"365-Day High Volume: {stock_data['365-Day High Volume']}\n")
            file.write(f"365-Day Low Volume: {stock_data['365-Day Low Volume']}\n")
            file.write(f"Market Cap: ₹{stock_data['Market Cap']:,.2f} thousand crores\n")
            
            file.write("\nLast 4 Quarters Revenue (in thousand crores):\n")
            for date, revenue in stock_data["Last 4 Quarters Revenue"].items():
                file.write(f"{date}: ₹{revenue:,.2f} thousand crores\n")
            
            file.write("\nLast 4 Quarters Profit (in thousand crores):\n")
            for date, profit in stock_data["Last 4 Quarters Profit"].items():
                file.write(f"{date}: ₹{profit:,.2f} thousand crores\n")
            
            file.write(f"\nSector: {stock_data['Sector']}\n")
            file.write(f"Industry: {stock_data['Industry']}\n")
            file.write(f"P/E Ratio: {stock_data['P/E Ratio']}\n")
            file.write("\n" + "-"*50 + "\n")

    print(f"\nStock information saved to {csv_file} and {text_file}")

def plot_candlestick_chart(ticker, period='1mo'):
    # Retrieve historical market data
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    # Plotting the candlestick chart
    mpf.plot(hist, type='candle', style='charles', volume=True)

def plot_revenue_and_profit(stock_data, revenues, profits):
    quarters = ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"]
    revenue_labels = [f"{quarters[i]} Revenue" for i in range(len(revenues))]
    profit_labels = [f"{quarters[i]} Profit" for i in range(len(profits))]
    
    plt.figure(figsize=(14, 7))

    # Plot Revenue
    plt.subplot(1, 2, 1)
    plt.bar(revenue_labels, list(revenues.values()), color='blue')
    plt.title(f"{stock_data['Stock Ticker']} - Last 4 Quarters Revenue")
    plt.xlabel("Quarter")
    plt.ylabel("Revenue (in thousand crores)")
    plt.xticks(rotation=45)

    # Plot Profit
    plt.subplot(1, 2, 2)
    plt.bar(profit_labels, list(profits.values()), color='green')
    plt.title(f"{stock_data['Stock Ticker']} - Last 4 Quarters Profit")
    plt.xlabel("Quarter")
    plt.ylabel("Profit (in thousand crores)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    tickers = input("Enter stock ticker symbols (comma separated): ").upper().split(',')
    
    # Retrieve and save stock information
    all_stock_data = []
    for ticker in tickers:
        stock_data, revenues, profits = get_stock_info(ticker.strip())
        all_stock_data.append(stock_data)
    
    save_to_files(all_stock_data)

    # Ask if the user wants to plot candlestick charts
    plot_charts = input("Do you want to plot candlestick charts? (yes/no): ").lower()
    
    if plot_charts == 'yes':
        for ticker in tickers:
            choose_period = input(f"Do you want to choose the period for {ticker.strip()}? (yes/no): ").lower()
            if choose_period == 'yes':
                period = input("Enter period ('1d', '5d', '1mo', '3mo', '6mo', 'ytd', 'max'): ").lower()
            else:
                period = '3mo'  # Default to 3 months if user doesn't want to choose
            plot_candlestick_chart(ticker.strip(), period)

    # Plot revenue and profit for each stock
    plot_revenue_profits = input("Do you want to plot revenue and profit graphs? (yes/no): ").lower()
    
    if plot_revenue_profits == 'yes':
        for stock_data in all_stock_data:
            revenues = stock_data["Last 4 Quarters Revenue"]
            profits = stock_data["Last 4 Quarters Profit"]
            plot_revenue_and_profit(stock_data, revenues, profits)
