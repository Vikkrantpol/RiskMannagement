# RiskMannagement

Trial26.py

Stock Data and Position Size Script

This Risk Management system is purely based on "Technical Analysis".
The Main and unique feature of the script is the risk will be always less than 0.25%.
Overview

The Idea behind Making the Risk Management system is to make quick positions, as the price moves very fast at the time of breakout or while taking support.
After taking insights from many great traders. I have built this Risk Management system so that traders can make quick positions, can set stop loss like professional traders, and can calculate risk quickly rather than wasting time on pen and paper. 

This Risk Management system is personally tested by me. This helped me a lot to make big positions quickly by analyzing risk on my capital. 
 
In this script, position sizing is defined in such a way that on any capital by using default stop loss the risk won't cross 0.25%. If the in the live trading session % up of the stock is less than 3.5% you can make a position in that stock.

This Python script helps investors fetch the latest stock price and percentage change from Yahoo Finance, calculate position size based on risk management principles, and save the data to both CSV and text files. It also offers options to calculate and set stop loss based on various criteria. 

Features

Fetch Stock Data: Retrieve the last trading day's closing price and percentage change for a given stock symbol from Yahoo Finance.
Calculate Position Size: Based on the percentage change in the stock price, the script calculates the position size, capital to be deployed, maximum risk, percentage risk per entire capital, and the number of shares to buy.
Set Stop Loss: Allows the user to set a stop loss based on:
Day's low price
Last session's closing price
Custom percentage of the current market price (CMP)
Exponential Moving Averages (EMAs) for various periods
Save Data: The data is saved to a CSV file and a text file for logging and future reference.

Example: 
Enter stock symbol (e.g., RELIANCE.NS): tcs.ns
Current Market Price (CMP): 4295.25
Percentage Change: 2.34%%
Position Size: 10.0%
Capital Deployed: Rs.144500.00
Max Risk: Rs.3381.30
% Risk per Entire Capital: 0.23%
No of Shares: 33

Select the stop loss option:
1. Day's Low Price
2. Last Session's Closing Price
3. Custom Stop Loss (Percentage of CMP)
4. EMA Stop Loss (Options: 5d, 7d, 9d, 12d, 15d, 18d, 21d, 50d)
Enter option number (1/2/3/4): 4
Available EMAs and their values:
5-day EMA: 4235.355778797868
7-day EMA: 4234.591235220912
9-day EMA: 4236.537392921574
12-day EMA: 4237.396694020519
15-day EMA: 4233.705697301452
18-day EMA: 4226.167799814463
21-day EMA: 4216.091162380403
50-day EMA: 4112.182900252501
Enter the EMA days you want to use (choose from 5, 7, 9, 12, 15, 18, 21, 50): 50
Date Time: 2024-08-15 18:42:32
Stock: tcs.ns
Price: 4295.25
Change: 2.34%
Position Size: 10.0%
Capital Deployed: Rs.144500.00
Max Risk: Rs.6041.21
% Risk on Deployed Capital: 4.18%
% Risk per Entire Capital: 0.42%
No of Shares: 33
Stop Loss: 4112.18
Data saved to stock_data_and_position_size_log.csv.
Data saved to stock_data_and_position_size_log.txt.

In this example, the default capital is 1445,000 Rupees
After entering the symbol of the stock the CMP, % Up, Position Size, Max Risk, deployed capital, % risk per entire capital, and the number of shares will be printed.
Further, users can select the option to set stop loss. Then user will get the output of modified entities chosen by the user.


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


