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
        for initial_capital in [100000.0]: # Config value ideally
            for name, data in self.pm.portfolios.items():
                data["cash"] = initial_capital
                data["holdings"] = {}
                data["history"] = []
                data["active_trades"] = []
                data["total_value"] = initial_capital
        
        print(f"--- New Challenge Week Started: {self.week_start} ---")

    def check_status(self):
        """
        Checks if the week is over.
        """
        if not self.is_active:
            self.start_new_week()
            return
            
        now = datetime.datetime.now()
        if now >= self.week_end:
            self.end_week()

    def end_week(self):
        """
        Declares winners and stops execution until restart.
        """
        print("--- Challenge Week Ended ---")
        summary = self.pm.get_portfolio_summary()
        winner = summary[0]
        print(f"Winner: {winner['name']} with {winner['return']}% return")
        
        # Restart immediately for the demo
        self.start_new_week()
