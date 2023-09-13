# Backtesting-SMA-App
Backtest your Fast/Slow SMA CrossOver Strategy for your desired Asset with this web app.

## Introduction

This application helps you backtest the popular 'Fast/Slow SMA crossover' strategy and compare it with a buy-and-hold strategy and a choosen benchmark.
It displays the backtested results, including the total return and a chart showing the strategy's performance.

Access the app by clicking here: https://backtesting-sma.streamlit.app/

![screenshot](https://github.com/acbouzas/Backtesting-SMA-App/blob/main/images/App%20Screenshot.png)

## How It Works

Here's an example of how the app works:

1. Enter the asset ticker (e.g., AAPL).

2. Enter the starting date (e.g., 2020-01-01).

3. Configure the SMA values (e.g., long SMA: 150, short SMA: 10).

4. Choose a benchmark (e.g., SPY).

5. Enjoy the results!

## Requirements

Before running the code, you need to install the following Python libraries:

- yfinance
- pandas
- streamlit
- numpy
