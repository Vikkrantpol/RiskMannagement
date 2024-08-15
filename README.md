# RiskMannagement
Risk Management with various and unique features like virtual portfolio, plot of Darvas box theory, etc.

52Week_Breakout.py is one of the many screeners. This script scans all the 1981 stock symbols from the file EQUITY_L.csv and identifies the names of the stocks that are at the fresh 52-week breakout, shortlists the names of the stocks, and saves them in the new CSV file called 52_Week_Breakout.csv.

Doji11.py is also one of the many screeners. This script scans all the 1981 stock symbols from the file EQUITY_L.csv and identifies the names of the stocks that formed a minimum of one doji in the last 5 trading sessions, shortlists the names of the stocks, and saves them in the new CSV file called doji_candles_detection_results.csv. And saves the chart of them also in the new directory.

Golden_crossover1.py is one of the many screeners. This script scans all the 1981 stock symbols from the file EQUITY_L.csv and identifies the names of the stocks in which golden crossover has happened recently. And gives brief information about them like date, prices, etc in a separate CSV file (golden_cross_results.csv).

Plot4.py will give the candle stick plot of the entered stock name by the user. Users can choose trading sessions and timeframes in this script.

Stockinfo6.py - After entering the name of the stock user will get the following things:
 1. 365-day High/Low price,
 2. 365-day High/Low Volume,
 3. Market cap of the firm,
 4. Revenue for the last four quarters,
 5. Profit of the last four quarters,
 6. Sector & industry,
 7. PE ratio,
 8. Chart of the stock as well.


Trial25.py - The user has to enter the ticker of the stock. This script will calculate the Risk so that the risk on the entire capital won't cross 0.25% (For the default position sizing)

