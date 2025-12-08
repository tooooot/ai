import datetime

class ChallengeEngine:
    def __init__(self, portfolio_manager):
        self.pm = portfolio_manager
        self.week_start = None
        self.week_end = None
        self.is_active = False

    def start_new_week(self):
        """
        Resets portfolios and starts a new challenge week.
        """
        self.week_start = datetime.datetime.now()
        self.week_end = self.week_start + datetime.timedelta(days=7) # Sunday to Thursday usually
        self.is_active = True
        
        # Reset Logic
        import random
        for initial_capital in [100000.0]: # Config value ideally
            for name, data in self.pm.portfolios.items():
                # SEED INITIAL VARIATION FOR DEMO
                variation = random.uniform(-1.5, 2.5) # -1.5% to +2.5%
                seeded_cash = initial_capital * (1 + (variation / 100))
                
                data["cash"] = seeded_cash
                data["holdings"] = {}
                data["history"] = []
                data["active_trades"] = []
                data["total_value"] = seeded_cash
        
        print(f"--- New Challenge Week Started: {self.week_start} ---")

    def check_status(self):
        """
        Checks if the week is over and triggers random shocks.
        """
        if not self.is_active:
            self.start_new_week()
            return
            
        now = datetime.datetime.now()
        if now >= self.week_end:
            self.end_week()
            
        # Random Event Trigger (1 in 20 chance per check)
        import random
        if random.randint(1, 20) == 1:
            self.trigger_random_event()

    def trigger_random_event(self):
        """
        Simulate a market shock or boost.
        """
        events = [
            {"name": "Oil Surge", "impact": 1.02, "msg": "ارتفاع أسعار النفط يدعم السوق!"},
            {"name": "Tech Rally", "impact": 1.03, "msg": "قطاع التقنية يقود الارتفاعات!"},
            {"name": "Global Selloff", "impact": 0.97, "msg": "موجة بيع عالمية تؤثر على السوق."},
            {"name": "Rate Hike Fear", "impact": 0.98, "msg": "مخاوف الفائدة تضغط على المؤشر."},
        ]
        
        event = random.choice(events)
        print(f"!!! MARKET EVENT: {event['name']} - {event['msg']}")
        
        # Apply impact to all active portfolios (Simulated)
        for name, data in self.pm.portfolios.items():
            # Add random variation to the impact so not everyone moves exactly same
            variation = random.uniform(0.99, 1.01)
            data["total_value"] *= (event["impact"] * variation)

    def end_week(self):
        """
        Declares winners and stops execution until restart.
        """
        print("--- Challenge Week Ended ---")
        summary = self.pm.get_portfolio_summary()
        if summary:
            winner = summary[0]
            print(f"Winner: {winner['name']} with {winner['return']}% return")
        else:
            print("No active portfolios.")
        
        # Restart immediately for the demo
        self.start_new_week()
