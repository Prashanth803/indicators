from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np
# import schedule
import os

class OBV:
    def __init__(self,stocks,close):
        self.stocks = stocks
        self.close = close

    def append_to_csv(self,df, file_path):
        mode = 'w' if not os.path.isfile(file_path) else 'a'
        df.to_csv(file_path, mode=mode, header=mode=='w', index=False)
        print("Data appended successfully to", file_path)

    # Function to generate simulated stock data
    def generate_stock_data(self,symbol, start_price, num_minutes=30*24*60):
        start_time = datetime.now() - timedelta(days=30)
        current_price = start_price
        stock_data = []

        for i in range(num_minutes):
            open_price = current_price
            high_price = open_price + random.uniform(0, 0.2)
            low_price = open_price - random.uniform(0, 0.2)
            close_price = random.uniform(low_price, high_price)
            volume = random.randint(1, 10)
            current_price = close_price
            timestamp = start_time + timedelta(minutes=i)
            stock_data.append({
                "symbol": symbol,
                "timestamp": timestamp,
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": volume
            })
        
        return stock_data

    # Function to calculate OBV
    def calculate_obv(self,df):
        obv = [0]
        for i in range(1, len(df)):
            if df['close'].iloc[i] > df['close'].iloc[i-1]:
                obv.append(obv[-1] + df['volume'].iloc[i])
            elif df['close'].iloc[i] < df['close'].iloc[i-1]:
                obv.append(obv[-1] - df['volume'].iloc[i])
            else:
                obv.append(obv[-1])
        
        df['OBV'] = pd.Series(obv, index=df.index)
        return df

    def calculate_obv_strategy(self,df, obv_ma_period=20):
        avg = df['OBV'].ewm(obv_ma_period).mean()
        df['Buy_signal'] = np.nan
        df['Sell_signal'] = np.nan

        for i in range(1, len(df)):
            if df['OBV'].iloc[i] > avg.iloc[i] and df['OBV'].iloc[i-1] <= avg.iloc[i-1]:
                df.loc[df.index[i],'Buy_signal'] = 1
                df.loc[df.index[i],'Sell_signal'] = 0
            elif df['OBV'].iloc[i] < avg.iloc[i] and df['OBV'].iloc[i-1] >= avg.iloc[i-1]:
                df.loc[df.index[i],'Sell_signal'] = 1
                df.loc[df.index[i],'Buy_signal'] = 0
            else:
                df.loc[df.index[i],'Buy_signal'] = 0
                df.loc[df.index[i],'Sell_signal'] = 0
        
        return df

    def group(self,frame):
        new_stock_data = self.generate_stock_data("Mishra", self.close, frame)
        new_stock_data=pd.DataFrame(new_stock_data)
        self.stocks=pd.concat([self.stocks,new_stock_data],ignore_index=False)
        df = self.calculate_obv(self.stocks)
        df = self.calculate_obv_strategy(df, 5)
        df=df.iloc[-len(new_stock_data):]
        self.close = df['close'].iloc[-1]
        # self.append_to_csv(df, 'obv.csv')
        return df

    def run(self):
        # schedule.every(1).minutes.do(self.group, 5)
        # current_time = datetime.now()
        # future_time = current_time + timedelta(hours=24)
        # while datetime.now() < future_time:
        #     schedule.run_pending()
        new_stock=self.group(1)
        return new_stock

# if __name__ == "__main__":
#     stocks = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
#     close = 200
#     obv = OBV(stocks, close)
#     obv.run()
    # Schedule the group function
    