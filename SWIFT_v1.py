import pandas as pd # type: ignore
import requests
import time
from decouple import config
import MetaTrader5 as mt5
from datetime import datetime
import talib as ta 

if not mt5.initialize(login=156984028, server="Exness-MT5Trial",password="Saadsr@1234"):
    print("Failed to initialize MT5")
    mt5.shutdown()

symbol = "BTCUSDm"
timeframe = mt5.TIMEFRAME_M5  
num_candles = 5  
end_time = datetime.now()
start_time = end_time - pd.Timedelta(hours=0.416666667)
candles = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)
#THE CANDLES DATA PD DATAFRAME
candles_data = pd.DataFrame(candles)
##############################
candles_data['time'] = pd.to_datetime(candles_data['time'], unit='s')
candles_data['lower_band'], candles_data['midlle_band'], candles_data['upper_band'] = ta.BBANDS(candles_data['close'], timeperiod=20,nbdevup=2, nbdevdn=2, matype=0)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TRADING ORDERS PARAMETERS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
lot = 0.01
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 0
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 10000* point,
    "tp": price + 20000* point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,
}


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Functions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def latestCandle(x):
    y=x.iloc[0]
    return y

def theCandleBefore(x):
    y=x.iloc[1]
    return y

def is_bearish(x):
    if x['open']>x['close']:
        return True
    else:
        return False
    
def is_bullish(x):
    if x['open']<x['close']:
        return True
    else:
        return False

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


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Excution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
current_time = time.strftime("%Y-%m-%d %H:%M:%S")
x=current_time.split(' ')
y=x[1].split(':')
current_minute=int(y[1])
timer=True

while(timer):
    if current_minute%5!=0:
        pass
    else:
        if(BB_overbought(latestCandle(candles_data))):
            request = {    
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price - 10000* point,
            "tp": price + 10000* point,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
                      }
            mt5.order_send(request)
        if(BB_oversold(latestCandle(candles_data))):
            
            request = {    
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 10000* point,
            "tp": price + 10000* point,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
                      }
            mt5.order_send(request)
            
        time.sleep(300)
        
        
        



        
        
        
        
        
        