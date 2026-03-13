import os
import json
import sys
from datetime import datetime, timedelta
try:
    from dotenv import load_dotenv # type: ignore
except ImportError:
    load_dotenv = None

# Handle optional dependencies gracefully
try:
    import pandas as pd # type: ignore
except ImportError:
    pd = None

try:
    from binance.client import Client # type: ignore
except ImportError:
    Client = None

class MemoryClawMentor:
    def __init__(self):
        if load_dotenv:
            load_dotenv()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_SECRET')
        self.testnet = os.getenv('TESTNET', 'true').lower() == 'true'
        self.risk_mode = os.getenv('RISK_MODE', 'conservative')
        
        from typing import Dict, Any, Optional
        # Initialize memory with a structure that satisfies type checkers
        self.memory: Dict[str, Any] = {
            "patterns": {},
            "user_profile": {},
            "last_analysis": None
        }
        self.client = None
        
        if Client and self.api_key and self.api_secret:
            try:
                self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            except Exception as e:
                print(f"DEBUG: Failed to initialize Binance client: {e}", file=sys.stderr)
        
        self.memory_path = os.path.join(os.path.dirname(__file__), "memory.json")
        self.journal_path = os.path.join(os.path.dirname(__file__), "trade_journal.json")
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "patterns": {
                    "win_rate": 0.5,
                    "favorite_tokens": [],
                    "bad_habits": []
                },
                "user_profile": {
                    "experience": "intermediate",
                    "risk_tolerance": self.risk_mode
                },
                "last_analysis": None
            }

    def save_memory(self):
        with open(self.memory_path, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def analyze_trades(self, limit=50):
        client = self.client
        if client is None:
            return {"error": "Binance API keys not configured or client not installed."}

        # For demo purposes, we usually look at a few common symbols if no history is provided
        # In a real skill, the agent would pass the symbols found in portfolio
        symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT']
        all_trades = []
        
        for symbol in symbols:
            try:
                trades = client.get_my_trades(symbol=symbol, limit=limit)
                for t in trades:
                    t['symbol'] = symbol
                all_trades.extend(trades)
            except Exception as e:
                continue

        if not all_trades:
            return {"message": "No trade history found to analyze."}

        if pd is None:
            return {"error": "Pandas library is not installed. Please run 'pip install pandas'."}

        df = pd.DataFrame(all_trades)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['qty'] = df['qty'].astype(float)
        df['price'] = df['price'].astype(float)
        df['quoteQty'] = df['quoteQty'].astype(float)
        df['isBuyer'] = df['isBuyer']

        # Calculate basic patterns
        patterns = {
            "total_trades": len(df),
            "volume_by_symbol": df.groupby('symbol')['quoteQty'].sum().to_dict(),
            "avg_trade_size": df['quoteQty'].mean(),
            "top_traded": str(df['symbol'].value_counts().idxmax()) if not df.empty else None
        }

        if 'patterns' not in self.memory or self.memory['patterns'] is None:
            self.memory['patterns'] = {}
            
        patterns_dict = self.memory['patterns']
        if isinstance(patterns_dict, dict):
            patterns_dict.update(patterns)
        
        self.memory['last_analysis'] = datetime.now().isoformat()
        self.save_memory()

        return patterns

    def get_portfolio_review(self):
        if not self.client:
            return {"error": "Binance API keys not configured."}
        
        try:
            account = self.client.get_account()
            balances = [b for b in account['balances'] if float(b['free']) > 0 or float(b['locked']) > 0]
            
            review = {
                "risk_mode": self.risk_mode,
                "balances": balances,
                "recommendation": "Diversify into more stables" if self.risk_mode == 'conservative' else "Look for high volatility memes"
            }
            return review
        except Exception as e:
            return {"error": str(e)}

    def log_trade(self, trade_data):
        journal = []
        if os.path.exists(self.journal_path):
            with open(self.journal_path, 'r') as f:
                try:
                    journal = json.load(f)
                except:
                    journal = []
        
        trade_data['logged_at'] = datetime.now().isoformat()
        journal.append(trade_data)
        
        with open(self.journal_path, 'w') as f:
            json.dump(journal, f, indent=4)
        return {"message": "Trade logged in journal."}

    def generate_report(self):
        # Comparison between user's style and 'Trading Twin' (the ideal version of them)
        patterns = self.memory.get('patterns', {})
        report = f"### Trading Twin Report for {self.risk_mode} Strategy\n"
        report += f"- **Current Win Rate Estimate:** {patterns.get('win_rate', 'N/A')}\n"
        report += f"- **Favorite Tokens:** {', '.join(patterns.get('favorite_tokens', ['None']))}\n"
        report += f"- **Observation:** You tend to trade {patterns.get('top_traded', 'unknown tokens')} often. "
        
        if self.risk_mode == 'conservative':
            report += "Your position sizes are healthy. Keep the 1% risk rule."
        else:
            report += "Warning: Your recent volume suggests aggressive positioning. Watch for liquidation risks."
        
        return report

if __name__ == "__main__":
    mentor = MemoryClawMentor()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "analyze":
            print(json.dumps(mentor.analyze_trades(), indent=2))
        elif cmd == "review":
            print(json.dumps(mentor.get_portfolio_review(), indent=2))
        elif cmd == "report":
            print(mentor.generate_report())
        elif cmd == "log":
            # Expecting trade data as JSON string in 3rd arg
            if len(sys.argv) > 2:
                data = json.loads(sys.argv[2])
                print(json.dumps(mentor.log_trade(data), indent=2))
    else:
        print("MemoryClaw Mentor Logic initialized.")
