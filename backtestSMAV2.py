# Import all pre-requisite python libraries to run this project
import yfinance as yf
import pandas as pd
import streamlit as st
import numpy as np
import plotly as px
import talib
import datetime
from ipdb import set_trace

# Function to validate the date format
def is_valid_date(date_str):
    try:
        # Attempt to parse the input string as a datetime with the desired format
        datetime.datetime.strptime(date_str, '%Y-%m-%d') 
        return True
    except ValueError:
        return False

def get_data (ticker, benchmark):
    
    # Download data from Yahoo-Finance
    data = yf.download(
        tickers = [ticker, benchmark], 
        period = 'max',
        interval = "1d", 
        ignore_tz=True,
        auto_adjust=True, # Adjust all fields by splits and dividends
        #group_by='ticker',
    )
    df = data['Close'].copy()
    df = pd.DataFrame(df)
    # Start from 2006-06-01 to get a complete month
    df['Buy & Hold'] = df[ticker].pct_change()
    df['Benchmark'] = df[benchmark].pct_change()
    # Fill the first row with zero
    df = df.fillna(0)
    return df


def get_signal(df):

    df['slow_ma'] = talib.SMA(df[ticker], slow_ma)
    df['fast_ma'] = talib.SMA(df[ticker], fast_ma)
    #df = df[~df['slow_ma'].isnull()]
    df = df.assign(
        signal = lambda x: np.where(x.fast_ma > x.slow_ma, 1, 0)
    )
    df['signal'] = df['signal'].shift(1, fill_value=0)
    df['Strategy'] = df['Buy & Hold']*df.signal
    keep_cols = ['Strategy', 'Buy & Hold', "Benchmark"]
    df_signal = df[keep_cols]
    df_signal = df_signal[starting_date:]

    return df_signal

def calc_ret(df_signal):

    # Total Return
    tot_return = ( (1 + df_signal).prod()-1 ) * 100
    tot_return = tot_return.to_frame().T.round(2)
    tot_return = tot_return.apply(lambda x: x.astype('str') + '%' )

    return tot_return


#Beggining of the App

header = st.container()
asset = st.container()
the_strategy = st.container()
#model_training = st.container()

benchmarks = ['', 'SPY', 'QQQ','BTC-USD','TLT','LQD'] 

with header:
    st.title('Fast/Slow SMA CrossOver - Backtesting App')

with asset:
    st.header('Choose your Asset and Benchmark to compare')
    sel_col, sel_col2 = st.columns(2)
    # Create a dynamic input for the user to select a stock symbol (ticker)
    ticker = sel_col.text_input('Write your desired Asset','AAPL').upper()
    starting_date = sel_col2.text_input('Write your desired starting date (YYYY-MM-DD)','')
    st.header('Choose your SMA Strategy')
    sel_col3, sel_col4 = st.columns(2)
    slow_ma = sel_col3.slider('Choose the long SMA Value', min_value=100, max_value=200, value=150, step=50)
    fast_ma = sel_col4.slider('Choose the short SMA Value', min_value=5, max_value=50, value=10, step=5)
    
    # Check if the input is valid
    if (starting_date == '') or not is_valid_date(starting_date):
        st.warning("To proceed, please confirm you've entered a valid Ticker and adhered to the date format: YYYY-MM-DD")
        pass
    else: 
        benchmark = st.selectbox('Choose your desired Benchmark', options= benchmarks, index=0, key='bench')
        if st.session_state['bench'] != '' : 
            st.header(f"Total Return")
            df = get_data(ticker, benchmark)
            #st.dataframe(df)
            df_signal = get_signal(df)
            #st.dataframe(df_signal)
            tot_return = calc_ret(df_signal)


            st.dataframe(tot_return, hide_index=True) 
            st.markdown('## Total Return Evolution')
            st.line_chart(100 * (1+df_signal).cumprod())

        else: 
            pass