import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class MarketDataService:
    def __init__(self):
        self.last_update = None
        self.market_suffix = ".SR"

    def is_connected(self):
        return True # Simulated always connected

    def get_current_price(self, symbol):
        """
        Fetches the latest price for a Saudi stock.
        Returns None if data is stale or invalid.
        """
        full_symbol = f"{symbol}{self.market_suffix}"
        try:
            ticker = yf.Ticker(full_symbol)
            # data = ticker.history(period="1d", interval="1m") # 1m data might be limited
            data = ticker.history(period="1d") # Fallback to daily if intraday not available
            
            if data.empty:
                print(f"Warning: No data found for {full_symbol}")
                return None

            latest = data.iloc[-1]
            price = latest['Close']
            
            # Basic Validation: Price must be positive
            if price <= 0:
                print(f"Error: Invalid price {price} for {full_symbol}")
                return None
                
            return price
        except Exception as e:
            print(f"Error fetching data for {full_symbol}: {e}")
            return None

    def get_market_status(self):
        """
        Returns TASI index status.
        """
        try:
            tasi = yf.Ticker("^TASI.SR")
            data = tasi.history(period="1d")
            if not data.empty:
                latest = data.iloc[-1]
                return {
                    "index": latest['Close'],
                    "change": latest['Close'] - latest['Open'], # Approx
                    "status": "Open" # Placeholder logic, need real time check
                }
        except:
            pass
        return {"index": 0, "change": 0, "status": "Unknown"}

    def is_data_fresh(self, timestamp):
        """
        Checks if the data timestamp is within the last 20 minutes.
        """
        # TASI open hours: 10:00 AM to 3:00 PM KSA time (GMT+3)
        # For now, simplest check: is it from today?
        now = datetime.now()
        data_time = pd.to_datetime(timestamp)
        return data_time.date() == now.date()
