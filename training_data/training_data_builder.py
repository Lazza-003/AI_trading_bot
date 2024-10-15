#train data builder

import ccxt

import pandas as pd
import time
from datetime import datetime
import csv

def test_fetch_data(exchange,symbol,timeframe,start_date,file_name):
   
    since = exchange.parse8601(start_date)  # Scegli una data recente
    limit = 1000
    all_data=[]
    while since<exchange.milliseconds():
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            if not ohlcv:
                break
            all_data.extend(ohlcv)
            since=ohlcv[-1][0] +1
            if len(ohlcv) > 0:
                print(f"Found data of: {datetime.fromtimestamp(since/1e9)}")
            else:
                print("Nessun dato trovato.")
            
            with open(file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in ohlcv:
                    writer.writerow(row)
        
        
        except Exception as e:
            print("Errore durante il fetch dei dati:", str(e))

    """df=pd.DataFrame(ohlcv,columns=['timestamp','open','high','low','close','volume'])
    df['timestamp']=pd.to_datetime(df['timestamp'],unit='ms')
    df.to_csv('BTC_USDT_1m_data.csv',index=False)
    """
            
    print("Dati salvati nel file 'BTC_USDT_1mdata.csv")


   
def main():
    #test_fetch_data()
    start_date = '2024-01-01T00:00:00Z'
    file_name = 'btc_usdt_data.csv'
    exchange = ccxt.binance()  # Puoi sostituire con un altro exchange se necessario
    symbol = 'BTC/USDT'
    timeframe = '1m'
    # Scrivere l'intestazione del file CSV solo se il file è vuoto
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Scaricare i dati e aggiungerli al file CSV
    test_fetch_data(exchange, symbol, timeframe, start_date, file_name)


main()