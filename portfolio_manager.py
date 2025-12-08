class PortfolioManager:
    def __init__(self, initial_capital=100000.0):
        # We will manage 10 portfolios, indexed by ID (0-9) or Name
        self.portfolios = {}
        strategy_names = [
            "رزين", "مقدام", "حصاد", 
            "برق", "قناص", "موج", 
            "مقتحم", "جوال", "عواطف", "محظوظ"
        ]
        
        for name in strategy_names:
            self.portfolios[name] = {
                "id": name,
                "cash": initial_capital,
                "holdings": {}, # symbol -> quantity
                "total_value": initial_capital, # cash + market_value_of_holdings
                "history": [],
                "active_trades": [] # List of open positions with goals
            }

    def execute_trade(self, strategy_name, action, symbol, price, quantity, reasoning, goals, extra_data={}):
        """
        Executes a trade and updates the portfolio.
        extra_data: dict for links, indicators, etc.
        """
        portfolio = self.portfolios.get(strategy_name)
        if not portfolio:
            return False, "Portfolio not found"

        total_cost = price * quantity
        
        if action == "BUY":
            if portfolio["cash"] >= total_cost:
                portfolio["cash"] -= total_cost
                current_qty = portfolio["holdings"].get(symbol, 0)
                portfolio["holdings"][symbol] = current_qty + quantity
                
                trade_record = {
                    "action": "BUY",
                    "symbol": symbol,
                    "price": price,
                    "quantity": quantity,
                    "timestamp": "Now", # timestamp
                    "reason": reasoning,
                    "verification_link": extra_data.get('verification_link'),
                    "rsi_value": extra_data.get('rsi_value'),
                    "goals": goals
                }
                portfolio["history"].append(trade_record)
                portfolio["active_trades"].append(trade_record)
                return True, "Buy Executed"
            else:
                return False, "Insufficient Funds"

        elif action == "SELL":
            current_qty = portfolio["holdings"].get(symbol, 0)
            if current_qty >= quantity:
                portfolio["holdings"][symbol] = current_qty - quantity
                portfolio["cash"] += total_cost
                # Remove from holdings if 0
                if portfolio["holdings"][symbol] == 0:
                    del portfolio["holdings"][symbol]
                    
                trade_record = {
                    "action": "SELL",
                    "symbol": symbol,
                    "price": price,
                    "quantity": quantity,
                    "timestamp": "Now",
                    "reason": reasoning,
                    "goals": None # Goals are for entry
                }
                portfolio["history"].append(trade_record)
                
                # Close active trade (logic to match sell with buy needs refinement for partial sells)
                portfolio["active_trades"] = [t for t in portfolio["active_trades"] if t["symbol"] != symbol]
                
                return True, "Sell Executed"
            else:
                return False, "Result Insufficient Holdings"
        
        return False, "Invalid Action"

    def get_portfolio_summary(self):
        """
        Returns a simplified list for the leaderboard.
        """
        summary = []
        for name, data in self.portfolios.items():
            summary.append({
                "name": name,
                "value": data["total_value"],
                "return": ((data["total_value"] - 100000) / 100000) * 100
            })
        # Sort by return DESC
        summary.sort(key=lambda x: x["return"], reverse=True)
        return summary
