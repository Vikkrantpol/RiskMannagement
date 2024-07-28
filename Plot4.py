import yfinance as yf
import mplfinance as mpf

def plot_candlestick_chart(ticker, period='3mo', interval='1d'):
    # Retrieve historical market data
    stock = yf.Ticker(ticker)
    try:
        hist = stock.history(period=period, interval=interval)
    except ValueError as e:
        if "is not supported" in str(e):
            print(f"Invalid input - interval={interval} is not supported.")
            print("Valid intervals: [1m, 3m, 5m, 30m, 45m, 1h, 1d, 1wk, 1mo]")
            return

    # Plotting the candlestick chart with stock name
    mpf.plot(hist, type='candle', style='charles', volume=True, title=ticker)

if __name__ == "__main__":
    ticker = input("Enter stock ticker symbol: ").upper()
    choose_period = input("Do you want to choose a period? (yes/no): ").strip().lower()

    if choose_period == 'yes':
        period = input("Enter period ('1d', '5d', '1mo', '3mo', '6mo', 'ytd', 'max'): ").strip().lower()
    else:
        period = '3mo'

    interval_options = {
        '1': '1m',
        '2': '3m',
        '3': '5m',
        '4': '30m',
        '5': '45m',
        '6': '1h',
        '7': '1d',
        '8': '1wk',
        '9': '1mo'
    }

    print("Choose an interval:")
    print("1: 1 minute")
    print("2: 3 minutes")
    print("3: 5 minutes")
    print("4: 30 minutes")
    print("5: 45 minutes")
    print("6: 1 hour")
    print("7: 1 day")
    print("8: 1 week")
    print("9: 1 month")

    interval_choice = input("Enter choice (1/2/3/4/5/6/7/8/9): ").strip()
    interval = interval_options.get(interval_choice, '1d')

    plot_candlestick_chart(ticker, period, interval)
