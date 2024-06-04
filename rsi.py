from datetime import datetime, timedelta
import pandas as pd
import random
import schedule 
import os

class RSI:
    def __init__(self,stocks,close):
        self.stocks = stocks
        self.close = close

# Initialize lists to store time and RSI values
    # def append_to_csv(self,df, file_path):
    #     mode = 'w' if not os.path.isfile(file_path) else 'a'
    #     df.to_csv(file_path, mode=mode, header=mode=='w', index=False)
    #     print("Data appended successfully to", file_path)

    # Function to generate stock data for 30 days (assuming 1 data point per minute)
    def generate_stock_data(self,symbol, start_price, num_minutes=30*24*60):
        stock_data = []
        current_price = start_price
        start_time = datetime.now()

        for i in range(num_minutes):  # 30 days of minute-by-minute data
            open_price = current_price
            high_price = open_price + random.uniform(0, 0.2)
            low_price = open_price - random.uniform(0, 0.2)
            close_price = random.uniform(low_price, high_price)
            volume = random.randint(1, 10)
            current_price = close_price

            timestamp = start_time + timedelta(minutes=i)

            stock_data.append({
                'symbol': symbol,
                'timestamp': timestamp,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })

        return stock_data

    # Function to fetch RSI
    def fetch_rsi(self,stock_data):
        data = pd.DataFrame(stock_data)
        data.set_index('timestamp', inplace=True)

        # Calculate RSI using pandas (example using close price)
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    # Function to update the plot
    def update_plot(self,frame):
        try:
            # Simulate receiving new stock data point
            new_stock_data = self.generate_stock_data('AAPL', self.close, frame)
            # Create DataFrame from new stock data
            new_stock_df = pd.DataFrame(new_stock_data)
            # Concatenate new stock data with existing DataFrame
            self.stocks = pd.concat([self.stocks, new_stock_df], ignore_index=True)
            rsi_values = self.fetch_rsi(self.stocks)
            
            # Use the latest RSI values
            rsi_values = rsi_values[-len(new_stock_df):]
            
            buy_signals = []
            sell_signals = []
            for rsi in rsi_values:
                if rsi < 30:
                    buy_signals.append('Buy')
                    sell_signals.append('None')
                elif rsi > 70:
                    sell_signals.append('Sell')
                    buy_signals.append('None')
                else:
                    buy_signals.append('None')
                    sell_signals.append('None')

            # Update new_stock_df DataFrame with RSI values and buy/sell signals
            new_stock_df['rsi'] = rsi_values.values
            new_stock_df['buy_signals'] = buy_signals
            new_stock_df['sell_signals'] = sell_signals
            
        
            self.close = new_stock_df.iloc[-1]['close']
            return new_stock_df
        except Exception as e:
            print(f"Error fetching or plotting data: {e}")

    def run(self):
    # Schedule update_plot function
        # schedule.every(1).minutes.do(self.update_plot, 5)
        new_stock_df=self.update_plot(1)
        return new_stock_df
        # # Run scheduled tasks until future_time is reached
        # current_time = datetime.now()
        # future_time = current_time + timedelta(hours=24)
        # while datetime.now() < future_time:
        #     schedule.run_pending()

# if __name__ == "__main__":
#     stocks = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
#     close = 200
#     rsi = RSI(stocks,close)
#     rsi.run()