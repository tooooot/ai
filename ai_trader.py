import random
from market_data import MarketDataService
from news_engine import NewsEngine
import pandas as pd
import ta

class AITrader:
    def __init__(self, market_service, news_service):
        self.market = market_service
        self.news = news_service
        self.strategies = {
            "رزين": self.conservative_strategy,
            "مقدام": self.growth_strategy,
            "حصاد": self.dividend_strategy,
            "برق": self.scalper_strategy,
            "قناص": self.mean_reversion_strategy,
            "موج": self.trend_follower_strategy,
            "مقتحم": self.volatility_breakout_strategy,
            "جوال": self.sector_rotator_strategy,
            "عواطف": self.sentiment_strategy,
            "محظوظ": self.random_strategy
        }

    def get_decision(self, strategy_name, portfolio_state):
        """
        Returns a decision for a given strategy.
        Returns: {action, symbol, reason, goals}
        """
        strategy_func = self.strategies.get(strategy_name)
        if strategy_func:
            return strategy_func(portfolio_state)
        return None

    # --- Strategy Implementations ---

    def conservative_strategy(self, portfolio):
        # Logic: Buy low beta, stable stocks (Al Rajhi, STC, Aramco)
        # Reason: Safety first.
        symbol = "1120" # Al Rajhi
        price = self.market.get_current_price(symbol)
        
        if not price: return None
        
        # DEMO MODE: Aggressive Entry
        # Buy if we don't own it OR if we own it but have plenty of cash (DCA)
        if portfolio["cash"] > 2000:
            return {
                "action": "BUY",
                "symbol": symbol,
                "quantity": 10,
                "price": price,
                "reason": "سهم قيادي مستقر. مكرر الربحية ضمن النطاق الآمن. فرصة جيدة للتجميع (Demo Entry).",
                "verification_link": "https://www.saudiexchange.sa/wps/portal/tadawul/market-participants/issuers/issuers-directory/company-details/!ut/p/z1/?companySymbol=1120",
                "goals": {
                    "target_price": price * 1.05, # 5% target
                    "stop_loss": price * 0.98,    # 2% stop
                    "time_horizon": "1 Week"
                }
            }
        return {"action": "HOLD", "reason": "السوق متذبذب، نفضل الانتظار في الكاش.", "goals": None}

    def sentiment_strategy(self, portfolio):
        # Logic: Check news. If positive, buy related sector.
        news_items = self.news.fetch_latest_news()
        
        # Simple heuristic: If vast majority positive, buy Index ETF or Proxy
        positive_count = sum(1 for n in news_items if n["sentiment"] == "Positive")
        
        if positive_count >= 3:
            symbol = "2222" # Aramco (Proxy for market)
            price = self.market.get_current_price(symbol)
            if price and portfolio["cash"] > 2000:
                return {
                    "action": "BUY",
                    "symbol": symbol,
                    "quantity": 50,
                    "price": price,
                    "reason": f"رصدت {positive_count} أخبار إيجابية قوية تؤثر على قطاع الطاقة.",
                    "verification_link": "https://twitter.com/search?q=Aramco",
                    "goals": {
                        "target_price": price * 1.02, 
                        "stop_loss": price * 0.99,
                        "time_horizon": "2 Days"
                    }
                }
        return {"action": "HOLD", "reason": "لم أجد أخباراً محفزة كافية للدخول.", "goals": None}

    def mean_reversion_strategy(self, portfolio):
        # Logic: Buy RSI < 30
        symbol = "1010" # Riyad Bank
        # Need history from market_data (not implemented fully there, mocking logic)
        rsi = 25 # Simulated low RSI
        
        price = self.market.get_current_price(symbol)
        if price and rsi < 30 and portfolio["cash"] > 5000:
             return {
                "action": "BUY",
                "symbol": symbol,
                "quantity": 20,
                "price": price,
                "reason": f"مؤشر RSI وصل إلى {rsi} (تشبع بيعي). نتوقع ارتداداً فنياً قريباً.",
                "verification_link": "https://www.tradingview.com/chart/?symbol=TADAWUL:1010",
                "rsi_value": rsi, # For Visualizer
                "goals": {
                    "target_price": price * 1.03, 
                    "stop_loss": price * 0.97,
                    "time_horizon": "3 Days"
                }
            }
        return {"action": "HOLD", "reason": "المؤشرات الفنية في مناطق محايدة.", "goals": None}

    # ... Implement others similarly ...
    def growth_strategy(self, _): return {"action": "HOLD", "reason": "بحث عن أسهم نمو...", "goals": None}
    def dividend_strategy(self, _): return {"action": "HOLD", "reason": "بحث عن توزيعات...", "goals": None}
    def scalper_strategy(self, _): return {"action": "HOLD", "reason": "السيولة ضعيفة للمضاربة.", "goals": None}
    def trend_follower_strategy(self, _): return {"action": "HOLD", "reason": "السوق في مسار عرضي.", "goals": None}
    def volatility_breakout_strategy(self, _): return {"action": "HOLD", "reason": "التقلبات منخفضة.", "goals": None}
    def sector_rotator_strategy(self, _): return {"action": "HOLD", "reason": "تحليل أداء القطاعات...", "goals": None}
    
    def random_strategy(self, portfolio):
        if random.random() > 0.8 and portfolio["cash"] > 1000:
            symbol = "1180" # NCB
            price = self.market.get_current_price(symbol)
            if price:
                return {
                    "action": "BUY",
                    "symbol": symbol,
                    "quantity": 5,
                    "price": price,
                    "reason": "اختيار عشوائي (استراتيجية المقارنة).",
                    "goals": {
                        "target_price": price * 1.10,
                        "stop_loss": price * 0.90,
                        "time_horizon": "Random"
                    }
                }
        return {"action": "HOLD", "reason": "....", "goals": None}
