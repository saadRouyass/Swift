import pandas as pd
import MetaTrader5 as mt5
import MetaTrader5 as mt5
from datetime import datetime,timedelta
import talib as ta
import vectorbt as vbt
import matplotlib

if not mt5.initialize(login=156984028, server="Exness-MT5Trial",password="Saadsr@1234"):
    print("Failed to initialize MT5")
    mt5.shutdown()

def BB_overbought(x):
    if float(x['open'])>float(x['upper_band']) and float(x['close'])>float(x['upper_band']):
        return True
    else:
        return False

def BB_oversold(x):
    if float(x['open'])<float(x['lower_band']) and float(x['close'])<float(x['lower_band']):
        return True
    else:
        return False
#historical data
symbol = "BTCUSDm"
timeframe = mt5.TIMEFRAME_M5  
num_candles = 2016  
end_time = datetime.now()
start_time = end_time - timedelta(days=7)
candles = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)
#THE CANDLES DATA PD DATAFRAME
candles_data = pd.DataFrame(candles)
candles_data['upper_band'], candles_data['midlle_band'], candles_data['lower_band'] = ta.BBANDS(candles_data['close'], timeperiod=20,nbdevup=2, nbdevdn=2, matype=0)

entries=[]
exits=[]
for i in range(25,candles_data.shape[0]):
    exits=exits+[False]

for i in range(25,candles_data.shape[0]):
    entries= entries+[(BB_overbought(candles_data.iloc[i]) or BB_oversold(candles_data.iloc[i]))]
    if entries[i-25]==True:
        exits[i-25]=False
        exits[i-25+1]=True
   
portfolio = vbt.Portfolio.from_signals(candles_data[25:2016]['close'], entries, exits,init_cash=500)
print(portfolio.stats())
portfolio.plot().show()

        
        


